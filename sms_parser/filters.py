import re

def light_filter(sms_text: str, sender: str) -> bool:
    """
    Quickly filters out irrelevant SMS messages based on keywords and patterns.

    Args:
        sms_text: The text content of the SMS message.
        sender: The sender of the SMS message.

    Returns:
        True if the message is considered irrelevant, False otherwise.
    """
    sms_text_lower = sms_text.lower()

    # Discard messages based on keywords
    irrelevant_keywords = [
        "otp",
        "delivery",
        "order",
        "out for delivery",
        "is on the way",
        "verification code",
    ]
    if any(keyword in sms_text_lower for keyword in irrelevant_keywords):
        return True

    # Discard messages from specific sender patterns
    if sender.startswith("AD-"):
        return True

    # Discard messages based on patterns
    irrelevant_patterns = [
        r"Your \d+ is your One Time Password",
        r"Your Verification code",
        r"Your OTP is \d+",
        r".*delivery.*",
        r".*order.*",
    ]
    if any(re.match(pattern, sms_text) for pattern in irrelevant_patterns):
        return True

    return False

def is_banking_sms(sms_text: str) -> bool:
    """
    Checks if the SMS message is related to banking.

    Args:
        sms_text: The text content of the SMS message.

    Returns:
        True if the message is related to banking, False otherwise.
    """
    sms_text_lower = sms_text.lower()
    banking_keywords = [
        "debited",
        "credited",
        "balance",
        "account",
        "transaction",
        "payment",
        "transfer",
        "deposit",
        "withdrawal",
        "bank",
        "credit card",
        "debit card",
        "loan",
        "emi",
        "upi"
    ]
    return any(keyword in sms_text_lower for keyword in banking_keywords)

def is_promotional(sms_text: str) -> bool:
    """
    Checks if the SMS message is promotional.

    Args:
        sms_text: The text content of the SMS message.

    Returns:
        True if the message is promotional, False otherwise.
    """
    sms_text_lower = sms_text.lower()
    promotional_keywords = [
        "offer",
        "discount",
        "sale",
        "cashback",
        "promo",
        "coupon",
        "reward",
        "exclusive",
        "limited time",
        "apply now",
        "get rs",
        "win rs",
        "shop now",
        "deal"
    ]
    return any(keyword in sms_text_lower for keyword in promotional_keywords)

def is_fraud(sms_text: str, sender: str) -> bool:
    """
    Checks if the SMS message is potentially fraudulent.

    Args:
        sms_text: The text content of the SMS message.
        sender: The sender of the SMS message.

    Returns:
        True if the message is potentially fraudulent, False otherwise.
    """
    sms_text_lower = sms_text.lower()
    fraud_keywords = [
        "block upi",
        "not you?",
        "suspicious activity",
        "fraudulent",
        "unauthorized",
        "urgent action",
        "click here",
        "verify now",
        "confirm your details",
        "account locked",
        "account blocked"
    ]
    if "https://" in sms_text_lower or "http://" in sms_text_lower:
        return True
    return any(keyword in sms_text_lower for keyword in fraud_keywords)

def is_relevant(sms_text: str, sender: str) -> bool:
    """
    Checks if the SMS message is relevant for further processing by the LLM.

    Args:
        sms_text: The text content of the SMS message.
        sender: The sender of the SMS message.

    Returns:
        True if the message is relevant, False otherwise.
    """
    if light_filter(sms_text, sender):
        return False
    if is_fraud(sms_text, sender):
        return True
    if is_banking_sms(sms_text):
        return True
    if is_promotional(sms_text):
        return False
    return True