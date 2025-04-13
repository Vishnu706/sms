#!/usr/bin/env python3

import google.generativeai as genai
from sms_parser.core.logger import get_logger
from sms_parser.core.config import GEMINI_API_KEY
from sms_parser.data_loader import load_data_from_csv
from sms_parser.helpers import _extract_json_from_response, _fallback_regex_parse, _enhance_parsing_with_csv_data, _extract_merchant_name
from typing import Optional, Dict, Any
from sms_parser.filters import light_filter, is_fraud
from sms_parser.storage import save_parsed_data, save_fraud_message
from sms_parser.database import DatabaseManager


class SmsParser:
    def __init__(self):
        self.logger = get_logger(__name__)
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
            self.logger.info("Gemini API configured successfully with model: gemini-1.5-pro")
        except Exception as e:
            self.logger.error(f"Failed to configure Gemini API: {e}")
            self.gemini_model = None
        load_data_from_csv()

    def parse_sms(self, sms_text: str, sender: Optional[str] = None, db_manager: Optional[DatabaseManager] = None) -> Dict[str, Any]:
        """Parse SMS text using Gemini API with light filter and fraud detection."""
        sender = sender or "Unknown"
        result: Dict[str, Any] = {"raw_sms": sms_text, "sender": sender}

        # Apply light filter
        if light_filter(sms_text, sender):
            result["light_filter_response"] = "Discarded by light filter"
            self.logger.info(f"SMS from {sender} discarded by light filter: {sms_text[:50]}...")
            # Add to database as discarded
            if db_manager:
                db_manager.insert_transaction(result)
            return result

        try:
            if is_fraud(sms_text, sender):
                result["is_fraud"] = True
                result["light_filter_response"] = "Passed light filter, identified as fraud"
                result["merchant_name"] = _extract_merchant_name(sms_text)
                save_fraud_message(result)
                self.logger.warning(f"Potential fraud SMS from {sender}: {sms_text[:50]}...")
                # Add to database as fraud
                if db_manager:
                    db_manager.insert_fraud_message(result)
                return result

            else:
                result["light_filter_response"] = "Passed light filter"
                # Generate prompt for Gemini API
                prompt = f"""Parse this SMS and return a JSON object with the following fields:
                - message_type: transaction, balance_update, bill_payment, transfer, subscription, financial, security_alert, or unknown
                - transaction_type: debit, credit, refund, transfer, bill, emi, or unknown
                - amount: numeric value or null
                - merchant_name: string or null
                - account_masked: string or null
                - date: YYYY-MM-DD format or null
                - available_balance: numeric value or null
                - description: string or null
                - is_fraud: boolean
                - fraud_indicators: list of strings or empty list
                - risk_score: numeric value between 0 and 1

                SMS: {sms_text}
                Sender: {sender}

                Return only the JSON object, no other text."""

                # Get response from Gemini API
                response = self.gemini_model.generate_content(prompt)
                response_text = response.text

                # Extract JSON from response
                parsed_data = _extract_json_from_response(response_text)

                # If JSON extraction failed, use fallback parser
                if not parsed_data:
                    self.logger.warning("Failed to extract JSON from API response, using fallback parser")
                    parsed_data = _fallback_regex_parse(sms_text, sender)

                # Enhance parsing with CSV data
                parsed_data = _enhance_parsing_with_csv_data(parsed_data, sms_text)

                # Merge parsed data with existing result
                result.update(parsed_data)

                save_parsed_data(result)
                self.logger.info(f"Successfully parsed SMS from {sender}: {sms_text[:50]}...")
                # Add to database
                if db_manager:
                    db_manager.insert_transaction(result)
                return result

        except Exception as e:
            self.logger.error(f"Error parsing SMS: {str(e)}")
            # Use fallback parser in case of error
            parsed_data = _fallback_regex_parse(sms_text, sender)
            return parsed_data