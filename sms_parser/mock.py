#!/usr/bin/env python3

import re
import json
import datetime
from typing import Dict, Any, Optional


def generate_mock_response(sms_text: str, sender: Optional[str] = None) -> Dict[str, Any]:
    """Generate a mock response for testing purposes."""
    return {
        "message_type": "transaction",
        "transaction_type": "debit",
        "amount": 1000.0,
        "merchant_name": "Test Merchant",
        "account_masked": "XXXX1234",
        "date": "2024-03-12",
        "available_balance": 5000.0,
        "description": "Test transaction",
        "is_mock": True
    }


def get_mock_response(sms_text: str, sender: Optional[str] = None) -> Dict[str, Any]:
    """Generate mock response for testing without API key"""
    # Create a basic structure based on text content
    sms_lower = sms_text.lower()

    # Check if it looks like a transaction
    is_transaction = any(word in sms_lower for word in ["debited", "credited", "spent", "received", "transaction", "payment"])

    # Check if it looks promotional
    is_promotional = any(word in sms_lower for word in ["offer", "discount", "sale", "cashback", "exclusive", "limited time"])

    # Extract some basic information with simple regex
    amount_match = re.search(r"(?:Rs\.?|INR|₹)\s*([0-9,]+(?:\.[0-9]+)?)", sms_text)
    amount = 0.0
    if amount_match:
        try:
            amount = float(amount_match.group(1).replace(',', ''))
        except ValueError:
            pass

    # Create mock response
    if is_transaction:
        return {
            "is_banking_sms": True,
            "is_promotional": False,
            "transaction": {
                "transaction_type": "debit" if "debited" in sms_lower or "spent" in sms_lower else "credit",
                "amount": amount if amount > 0 else 1000.0,
                "merchant_name": "",
                "account_masked": "XX1234" if "xx" in sms_lower or "account" in sms_lower else "",
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "available_balance": 0.0
            },
            "metadata": {
                "parse_method": "mock",
                "raw_sms": sms_text,
                "sender": sender
            }
        }
    elif is_promotional:
        return {
            "is_banking_sms": False,
            "is_promotional": True,
            "promo_score": 0.85,
            "promotion": {
                "merchant": "",
                "offer": "",
                "valid_until": ""
            },
            "metadata": {
                "parse_method": "mock",
                "raw_sms": sms_text,
                "sender": sender
            }
        }
    else:
        return {
            "is_banking_sms": False,
            "is_promotional": False,
            "category": "Uncategorized",
            "metadata": {
                "parse_method": "mock",
                "raw_sms": sms_text,
                "sender": sender
            }
        }