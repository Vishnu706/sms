#!/usr/bin/env python3

from enhanced_sms_parser import parse_sms, detect_fraud_indicators
from typing import Dict, Any

# Get user input
sms_text: str = input("Enter the SMS message: ")
sender: str = input("Enter the sender: ")

# Process the SMS
parsed_data: Dict[str, Any] = parse_sms(sms_text, sender)
fraud_results: Dict[str, Any] = detect_fraud_indicators(sms_text, sender, parsed_data)

# Print the results
print(f"SMS: {sms_text}")
print(f"Parsed Data: {parsed_data}")
print(f"Fraud Detection: {fraud_results}")