#!/usr/bin/env python3

import json
import datetime
import os
from typing import Dict, Any

from sms_parser.core.logger import get_logger

# Add constant for JSON file path
PARSED_SMS_FILE = "parsed_sms_data.json"
FRAUD_MESSAGES_FILE = "fraud_messages.json"


# Get logger
logger = get_logger(__name__)


def save_parsed_data(parsed_data: Dict[str, Any]) -> None:
    """Save parsed SMS data to a JSON file."""
    try:
        # Create the file if it doesn't exist
        if not os.path.exists(PARSED_SMS_FILE):
            with open(PARSED_SMS_FILE, 'w') as f:
                json.dump([], f)

        # Read existing data
        with open(PARSED_SMS_FILE, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        # Add timestamp to parsed data
        parsed_data['parsed_timestamp'] = datetime.datetime.now().isoformat()

        # Append new data
        existing_data.append(parsed_data)

        # Write back to file
        with open(PARSED_SMS_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)

        logger.info(f"Successfully saved parsed data to {PARSED_SMS_FILE}")
    except Exception as e:
        logger.error(f"Error saving parsed data: {str(e)}")


def save_fraud_message(fraud_message: Dict[str, Any]) -> None:
    """Save fraud messages to a separate JSON file."""
    try:
        # Create the file if it doesn't exist
        if not os.path.exists(FRAUD_MESSAGES_FILE):
            with open(FRAUD_MESSAGES_FILE, 'w') as f:
                json.dump([], f)

        # Read existing data
        with open(FRAUD_MESSAGES_FILE, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

        # Add timestamp to fraud message
        fraud_message['saved_timestamp'] = datetime.datetime.now().isoformat()

        # Append new data
        existing_data.append(fraud_message)

        # Write back to file
        with open(FRAUD_MESSAGES_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)

        logger.info(f"Successfully saved fraud message to {FRAUD_MESSAGES_FILE}")
    except Exception as e:
        logger.error(f"Error saving fraud message: {str(e)}")