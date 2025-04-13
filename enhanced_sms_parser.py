import re
from typing import Dict, Any, Optional

def detect_fraud_indicators(sms_text: str, sender: Optional[str] = None, transaction_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Analyze an SMS for potential fraud indicators

    Args:
        sms_text: The SMS text to analyze
        sender: The sender ID of the SMS
        transaction_data: Optional transaction data extracted from the SMS

    Returns:
        Dictionary containing fraud detection results
    """
    # Initialize fraud detection result
    is_suspicious = False
    risk_level = "none"
    suspicious_indicators = []

    # Convert to lowercase for easier pattern matching
    text_lower = sms_text.lower()

    # Check sender validity - only mark as suspicious if sender exists but is suspicious
    is_valid_sender = True
    if sender and sender.strip():
        # Simple bank sender validation (could be expanded)
        bank_senders = [
            "SBIINB", "HDFCBK", "ICICIB", "AXISBK", "KOTAKB", "YESBNK", "INDBNK",
            "PNBBNK", "BOIBNK", "CNRBNK", "AUBANK", "IDBBNK", "IOBBNK", "UCOBNK",
            "VK-SBIINB", "VK-HDFCBK", "VK-ICICIB", "VK-AXISBK", "VK-KOTAKB"
        ]
        is_valid_sender = any(bank_id in sender for bank_id in bank_senders)

        # Only mark as suspicious if sender exists but isn't recognized
        if not is_valid_sender:
            suspicious_indicators.append("unknown_sender")
            is_suspicious = True

    # Check for "block" in the correct context
    if "block" in text_lower:
        # Check for legitimate "block" phrases from known banks
        if is_valid_sender:
            legitimate_block_patterns = [
                r"sms block \w+ to \d+",  # SMS BLOCK XXXX to 9215676766
                r"send block to customer care",  # Send BLOCK to customer care
                r"block \w+ to",
                r"block this card",
                r"block your card",
                r"block card"
            ]
            if not any(re.search(pattern, text_lower) for pattern in legitimate_block_patterns):
                  suspicious_indicators.append("suspicious_block_usage")
                  is_suspicious = True

        # Check for aggressive/scam "block" context
        else:
            suspicious_block_patterns = [
                r"your account will be blocked",
                r"click now or you will be blocked",
                r"your account is blocked",
                r"account will be block",
                r"account is blocked",
                r"account will be deactivated",
                r"account is deactivated",
                r"your account will be deactivated",
            ]
            if any(re.search(pattern, text_lower) for pattern in suspicious_block_patterns):
                suspicious_indicators.append("threatening_block_usage")
                is_suspicious = True
            else:
                suspicious_indicators.append("block_usage")
                is_suspicious = True

    # Check for URLs and URL shorteners (very strong indicators of fraud)
    url_patterns = [
        "http", "www.", ".com", "bit.ly", "goo.gl", "tinyurl.com", "t.co",
        "short.ly", "ow.ly", "is.gd", "tiny.cc", "cutt.ly", "shorturl"
    ]
    contains_urls = False
    for pattern in url_patterns:
        if pattern in text_lower:
            contains_urls = True
            suspicious_indicators.append(f"url_{pattern.replace('.', '_')}")
            is_suspicious = True

    # Check for urgent/threatening language
    urgent_keywords = [
        "urgent", "immediately", "warning", "important", "action required", "last chance", "account suspended", "account will be blocked", "click here now", "verify now", "limited time offer", "security alert"
    ]
    if any(keyword in text_lower for keyword in urgent_keywords):
        suspicious_indicators.append("urgent_tone")
        is_suspicious = True

    # Check for excessive capitalization (common in spam)
    uppercase_chars = sum(1 for c in sms_text if c.isupper())
    total_chars = len(sms_text.strip())
    uppercase_ratio = uppercase_chars / total_chars if total_chars > 0 else 0

    if uppercase_ratio > 0.3 and total_chars > 20:  # More than 30% uppercase and long enough
        suspicious_indicators.append("language_excessive_caps")
        is_suspicious = True

    # Check for suspicious punctuation patterns
    if sms_text.count('!') > 2:
        suspicious_indicators.append("language_excessive_exclamation")
        is_suspicious = True
    
    # Check for credential/login phrases
    credential_phrases = [
        "password", "login", "verify identity", "verify details", "otp", "pin", 
        "security code", "access code", "validate", "authenticate"
    ]
    if any(phrase in text_lower for phrase in credential_phrases):
        suspicious_indicators.append("credential_phishing")
        is_suspicious = True

     # Check for KYC scams
    kyc_scam_phrases = [
        "kyc update", "account blocked", "account suspend", "kyc expir", "kyc verif",
        "update your kyc", "kyc not updated", "complete your kyc", "last date"
    ]
    if any(phrase in text_lower for phrase in kyc_scam_phrases):
        suspicious_indicators.append("kyc_scam")
        is_suspicious = True

    # Check account format if mentioned in SMS
    account_format_valid = True  # Default to true
    if transaction_data:
        # Check account_number or account_masked
        account_number = transaction_data.get("account_number", transaction_data.get("account_masked", ""))
        if account_number and not re.match(r'(X+\d+|XXXX\d+|\d{4})', account_number):
            account_format_valid = False

    # Evaluate transaction legitimacy
    transaction_seems_legitimate = True
    if transaction_data:
        # Get amount from various possible field names
        amount = (
            transaction_data.get("transaction_amount") or
            transaction_data.get("amount") or
            0
        )

        # Get merchant from various possible field names
        merchant = (
            transaction_data.get("merchant") or
            transaction_data.get("merchant_name") or
            ""
        )

        # Suspicious case: No merchant but has amount (only for non-UPI transactions)
        if amount > 0 and not merchant and "upi" not in text_lower and "neft" not in text_lower and "imps" not in text_lower:
            suspicious_indicators.append("missing_merchant")
            transaction_seems_legitimate = False
            is_suspicious = True

        # Suspicious case: Extremely high amount
        if amount > 100000:  # Arbitrary threshold
            suspicious_indicators.append("unusually_high_amount")
            transaction_seems_legitimate = False
            is_suspicious = True

    # Determine overall risk level with increased sensitivity
    if is_suspicious:
        # High risk: KYC scams, credential phishing, URLs in suspicious context
        if "kyc_scam" in suspicious_indicators or "credential_phishing" in suspicious_indicators or (contains_urls and "urgent_tone" in suspicious_indicators) :
            risk_level = "high"
        # Medium risk: Multiple indicators or prize scams
        elif len(suspicious_indicators) > 2 or "prize_scam" in suspicious_indicators:
            risk_level = "medium"
        # Low risk: Few indicators
        else:
            risk_level = "low"
        
    # Construct fraud detection result
    fraud_detection = {
        "is_suspicious": is_suspicious,
        "risk_level": risk_level,
        "suspicious_indicators": suspicious_indicators,
        "is_valid_sender": is_valid_sender,
        "is_valid_account_format": account_format_valid,
        "contains_urls": contains_urls,
        "transaction_seems_legitimate": transaction_seems_legitimate
    }

    return fraud_detection

def parse_sms(sms_text: str, sender: Optional[str] = None) -> Dict[str, Any]:
    """
    Parses an SMS message and extracts relevant information.

    Args:
        sms_text: The SMS message text.
        sender: The sender of the SMS message.

    Returns:
        A dictionary containing parsed information, including:
        - is_subscription: Boolean indicating if the message is a subscription.
        ... (other fields from previous implementation)
    """
    sms_text = sms_text.strip()
    parsed_data: Dict[str, Any] = {"is_subscription": False}

    # Subscription detection
    subscription_patterns = [
        r"AutoPay of ₹[\d,.]+ for (.+) has been processed",
        r"Your subscription for (.+) of ₹[\d,.]+ has been renewed",
        r"(.+) ₹[\d,.]+ has been debited via AutoPay",
        r"Auto-debit of ₹[\d,.]+ completed for (.+)",
        r"Recurring payment of ₹[\d,.]+ processed successfully"
    ]

    for pattern in subscription_patterns:
        if re.search(pattern, sms_text):
            parsed_data["is_subscription"] = True
            break

    # Transaction amount
    amount_match = re.search(r"₹([\d,\.]+)", sms_text)
    if amount_match:
        amount_str = amount_match.group(1).replace(",", "")
        parsed_data["transaction_amount"] = float(amount_str)
    else:
        parsed_data["transaction_amount"] = 0.0

    # Merchant information
    merchant_match = re.search(r"(?:for|to) (.+?) (?:of|has|₹|processed|completed|debited|via|at|on)", sms_text)
    if merchant_match:
        parsed_data["merchant"] = merchant_match.group(1).strip()
    else:
        parsed_data["merchant"] = "Unknown"

    # Account Masked (Last 4 digits or similar)
    account_match = re.search(r"(?:from|in) acct (?:ending|no\.) (?:(?:X{4}|\d{2,4})|X+\d+|\d{4})", sms_text, re.IGNORECASE)
    if account_match:
        account_info = account_match.group(1)
        if re.match(r"X{4}\d+", account_info, re.IGNORECASE) or re.match(r"\d{4}$", account_info):
            parsed_data["account_masked"] = account_info
        elif re.match(r"X+\d+", account_info, re.IGNORECASE):
            parsed_data["account_masked"] = account_info
        else:
            parsed_data["account_masked"] = "Unknown"
    else:
        parsed_data["account_masked"] = "Unknown"

    # Transaction ID or Reference Number
    transaction_id_match = re.search(r"(?:ref|txn|transaction)[\sno.:]*(\w+)", sms_text, re.IGNORECASE)
    if transaction_id_match:
        parsed_data["transaction_id"] = transaction_id_match.group(1)
    else:
        parsed_data["transaction_id"] = "Unknown"


    return parsed_data