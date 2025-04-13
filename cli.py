#!/usr/bin/env python3

import argparse
import pprint
from typing import Dict, Any, Optional
from sms_parser.parsers import SmsParser
from sms_parser.database import DatabaseManager
from sms_parser.filters import is_relevant

DB_FILE = "sms_data.db"


def process_single_sms(sms_text: str, output_file: str = None) -> Dict[str, Any]:
    """
    Process a single SMS message

    Args:
        sms_text: The SMS text to process
        output_file: Optional file to save output
        parser: SMS parser instance
        db_manager: Database manager instance

    Returns:
        The result dictionary
    """
    print(f"\nProcessing SMS: {sms_text}")
    print("-" * 50)

    try:
        if not parser or not db_manager:
            raise ValueError("Parser and DatabaseManager instances are required.")

        # Basic relevance check before parsing
        if not is_relevant(sms_text, "CLI Input"):
            print("SMS discarded as irrelevant by initial filter.")
            return {"status": "discarded", "sms": sms_text}

        # Parse the SMS using the parser instance and provide db_manager
        result = parser.parse_sms(sms_text, "CLI Input", db_manager=db_manager)
        print("Parsing complete.")
        return result

    except Exception as e:
        print(f"Error processing SMS: {e}")
        return {"error": str(e), "sms": sms_text}


def process_batch_file(file_path: str, output_file: str = None, parser: Optional[SmsParser] = None, db_manager: Optional[DatabaseManager] = None) -> None:
    """
    Process multiple SMS messages from a file

    Args:
        file_path: Path to a text file with one SMS per line
        output_file: Optional file to save output
        parser: SMS parser instance
        db_manager: Database manager instance
    """
    print(f"Processing SMS messages from file: {file_path}")

    try:
        if not parser or not db_manager:
            raise ValueError("Parser and DatabaseManager instances are required.")

        with open(file_path, 'r') as f:
            for line in f:
                sms_text = line.strip()
                if sms_text:  # Skip empty lines
                    print(f"\nProcessing SMS: {sms_text[:50]}...")
                    print("-" * 50)

                    # Basic relevance check before parsing
                    if is_relevant(sms_text, "Batch File"):
                        parser.parse_sms(sms_text, "Batch File", db_manager=db_manager)
                    else:
                        print("SMS discarded as irrelevant by initial filter.")

        print("Batch processing complete.")

    except Exception as e:
        print(f"Error processing batch file: {e}")
        print(f"Error processing batch file: {e}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="SMS Transaction Parser CLI")
    
    # Create command groups
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--sms", type=str, help="Single SMS message to process")
    group.add_argument("-f", "--file", type=str, help="File containing SMS messages (one per line)")
    
    # Output file option
    parser.add_argument("-o", "--output", help="Output file to save results (JSON)")
    
    # Parse arguments
    args = parser.parse_args()

    # Initialize parser and database manager
    sms_parser = SmsParser()
    db_manager = DatabaseManager(DB_FILE)

    try:
        # Process based on command
        if args.sms:
            result = process_single_sms(args.sms, args.output, sms_parser, db_manager)
            print("\nResult:")
            pprint.pprint(result)

        elif args.file:
            process_batch_file(args.file, args.output, sms_parser, db_manager)
            print("Finished processing batch file.")

        else:
            parser.print_help()

    finally:
        # Ensure database connection is closed
        if db_manager:
            db_manager.close_connection()

if __name__ == "__main__":
    main()