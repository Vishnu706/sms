import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_transactions_table()
        self.create_fraud_messages_table()

    def create_transactions_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_type TEXT,
                transaction_type TEXT,
                amount REAL,
                merchant_name TEXT,
                account_masked TEXT,
                date TEXT,
                available_balance REAL,
                description TEXT,
                is_fraud INTEGER,
                fraud_indicators TEXT,
                risk_score REAL,
                parsed_timestamp TEXT,
                is_subscription INTEGER,
                is_income INTEGER,
                category TEXT,
                transaction_status TEXT,
                failure_reason TEXT,
                as_of_date TEXT,
                bill_amount REAL,
                minimum_due REAL,
                due_date TEXT,
                loan_reference TEXT,
                company_name TEXT,
                offer_details TEXT,
                discount_percentage TEXT,
                promo_code TEXT,
                valid_until TEXT,
                bank_name TEXT,
                raw_sms TEXT,
                sender TEXT
            )
        """)
        self.conn.commit()

    def create_fraud_messages_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fraud_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_type TEXT,
                transaction_type TEXT,
                amount REAL,
                merchant_name TEXT,
                account_masked TEXT,
                date TEXT,
                available_balance REAL,
                description TEXT,
                is_fraud INTEGER,
                fraud_indicators TEXT,
                risk_score REAL,
                parsed_timestamp TEXT,
                is_subscription INTEGER,
                is_income INTEGER,
                category TEXT,
                transaction_status TEXT,
                failure_reason TEXT,
                as_of_date TEXT,
                bill_amount REAL,
                minimum_due REAL,
                due_date TEXT,
                loan_reference TEXT,
                company_name TEXT,
                offer_details TEXT,
                discount_percentage TEXT,
                promo_code TEXT,
                valid_until TEXT,
                bank_name TEXT,
                raw_sms TEXT,
                sender TEXT,
                light_filter_response TEXT
            )
        """)
        self.conn.commit()

    def insert_transaction(self, transaction_data):
        fraud_indicators_json = json.dumps(transaction_data.get('fraud_indicators', []))
        self.cursor.execute("""
            INSERT INTO transactions (
                message_type, transaction_type, amount, merchant_name, account_masked, date,
                available_balance, description, is_fraud, fraud_indicators, risk_score,
                parsed_timestamp, is_subscription, is_income, category, transaction_status,
                failure_reason, as_of_date, bill_amount, minimum_due, due_date, loan_reference,
                company_name, offer_details, discount_percentage, promo_code, valid_until,
                bank_name, raw_sms, sender
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction_data.get('message_type'),
            transaction_data.get('transaction_type'),
            transaction_data.get('amount'),
            transaction_data.get('merchant_name'),
            transaction_data.get('account_masked'),
            transaction_data.get('date'),
            transaction_data.get('available_balance'),
            transaction_data.get('description'),
            transaction_data.get('is_fraud', 0),
            fraud_indicators_json,
            transaction_data.get('risk_score', 0.0),
            transaction_data.get('parsed_timestamp'),
            transaction_data.get('is_subscription', 0),
            transaction_data.get('is_income', 0),
            transaction_data.get('category'),
            transaction_data.get('transaction_status'),
            transaction_data.get('failure_reason'),
            transaction_data.get('as_of_date'),
            transaction_data.get('bill_amount'),
            transaction_data.get('minimum_due'),
            transaction_data.get('due_date'),
            transaction_data.get('loan_reference'),
            transaction_data.get('company_name'),
            transaction_data.get('offer_details'),
            transaction_data.get('discount_percentage'),
            transaction_data.get('promo_code'),
            transaction_data.get('valid_until'),
            transaction_data.get('bank_name'),
            transaction_data.get('raw_sms'),
            transaction_data.get('sender')
        ))
        self.conn.commit()

    def insert_fraud_message(self, fraud_data):
        fraud_indicators_json = json.dumps(fraud_data.get('fraud_indicators', []))
        self.cursor.execute("""
            INSERT INTO fraud_messages (
                message_type, transaction_type, amount, merchant_name, account_masked, date,
                available_balance, description, is_fraud, fraud_indicators, risk_score,
                parsed_timestamp, is_subscription, is_income, category, transaction_status,
                failure_reason, as_of_date, bill_amount, minimum_due, due_date, loan_reference,
                company_name, offer_details, discount_percentage, promo_code, valid_until,
                bank_name, raw_sms, sender, light_filter_response
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fraud_data.get('message_type'),
            fraud_data.get('transaction_type'),
            fraud_data.get('amount'),
            fraud_data.get('merchant_name'),
            fraud_data.get('account_masked'),
            fraud_data.get('date'),
            fraud_data.get('available_balance'),
            fraud_data.get('description'),
            fraud_data.get('is_fraud', 0),
            fraud_indicators_json,
            fraud_data.get('risk_score', 0.0),
            fraud_data.get('parsed_timestamp'),
            fraud_data.get('is_subscription', 0),
            fraud_data.get('is_income', 0),
            fraud_data.get('category'),
            fraud_data.get('transaction_status'),
            fraud_data.get('failure_reason'),
            fraud_data.get('as_of_date'),
            fraud_data.get('bill_amount'),
            fraud_data.get('minimum_due'),
            fraud_data.get('due_date'),
            fraud_data.get('loan_reference'),
            fraud_data.get('company_name'),
            fraud_data.get('offer_details'),
            fraud_data.get('discount_percentage'),
            fraud_data.get('promo_code'),
            fraud_data.get('valid_until'),
            fraud_data.get('bank_name'),
            fraud_data.get('raw_sms'),
            fraud_data.get('sender'),
            json.dumps(fraud_data.get('light_filter_response'))
        ))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()