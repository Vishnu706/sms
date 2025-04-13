import os
import csv
from sms_parser.core.logger import get_logger

# Get logger
logger = get_logger(__name__)

# Global variables related to CSV files
MERCHANTS = []
MERCHANT_SHORT = []
BANKS = []
TRANSACTION_INDICATORS = []
FRAUD_INDICATORS = []
TRANSACTION_STATUS_KEYWORDS = []
BALANCE_UPDATE_KEYWORDS = []
BILL_STATEMENT_KEYWORDS = []
EMI_KEYWORDS = []
TRANSACTION_TYPES = []

# Define data paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
MERCHANT_FILE = os.path.join(DATA_DIR, "merchants.csv")
MERCHANT_SHORT_FILE = os.path.join(DATA_DIR, "merchant_short.csv")
BANK_FILE = os.path.join(DATA_DIR, "banks.csv")
TRANSACTION_TYPES_FILE = os.path.join(DATA_DIR, "transaction_types.csv")
TRANSACTION_INDICATORS_FILE = os.path.join(DATA_DIR, "transaction_indicator_keywords.csv")
FRAUD_FILE = os.path.join(DATA_DIR, "fraud.csv")
TRANSACTION_STATUS_FILE = os.path.join(DATA_DIR, "transaction_status_keywords.csv")
BALANCE_UPDATE_FILE = os.path.join(DATA_DIR, "balance_update_keywords.csv")
BILL_STATEMENT_FILE = os.path.join(DATA_DIR, "bill_statement_keywords.csv")
EMI_KEYWORDS_FILE = os.path.join(DATA_DIR, "loan_emi_keywords.csv")


def load_data_from_csv():
    """Load data from CSV files"""
    global MERCHANTS, MERCHANT_SHORT, BANKS, TRANSACTION_INDICATORS, FRAUD_INDICATORS
    global TRANSACTION_STATUS_KEYWORDS, BALANCE_UPDATE_KEYWORDS, BILL_STATEMENT_KEYWORDS, EMI_KEYWORDS, TRANSACTION_TYPES

    try:
        # Load merchant data
        if os.path.exists(MERCHANT_FILE):
            with open(MERCHANT_FILE, 'r') as f:
                reader = csv.DictReader(f)
                MERCHANTS = list(reader)
            logger.info(f"Loaded {len(MERCHANTS)} merchants from main file")

        # Load merchant short data
        if os.path.exists(MERCHANT_SHORT_FILE):
            with open(MERCHANT_SHORT_FILE, 'r') as f:
                reader = csv.DictReader(f)
                MERCHANT_SHORT = list(reader)
            logger.info(f"Loaded additional merchants from short file")

        # Load bank data
        if os.path.exists(BANK_FILE):
            with open(BANK_FILE, 'r') as f:
                reader = csv.DictReader(f)
                BANKS = list(reader)
            logger.info(f"Loaded {len(BANKS)} banks")

        # Load transaction types
        if os.path.exists(TRANSACTION_TYPES_FILE):
            with open(TRANSACTION_TYPES_FILE, 'r') as f:
                reader = csv.DictReader(f)
                TRANSACTION_TYPES = []
                for row in reader:
                    if 'transaction_type' in row:
                        TRANSACTION_TYPES.append(row['transaction_type'])
            logger.info(f"Loaded {len(TRANSACTION_TYPES)} transaction types")

        # Load transaction indicators
        if os.path.exists(TRANSACTION_INDICATORS_FILE):
            with open(TRANSACTION_INDICATORS_FILE, 'r') as f:
                TRANSACTION_INDICATORS = [line.strip() for line in f.readlines() if line.strip()]
            logger.info(f"Loaded {len(TRANSACTION_INDICATORS)} transaction indicators")

        # Load fraud indicators
        if os.path.exists(FRAUD_FILE):
            with open(FRAUD_FILE, 'r') as f:
                FRAUD_INDICATORS = [line.strip() for line in f.readlines() if line.strip()]
            logger.info(f"Loaded {len(FRAUD_INDICATORS)} fraud indicators")

        # Load transaction status keywords (failed, declined, etc.)
        if os.path.exists(TRANSACTION_STATUS_FILE):
            with open(TRANSACTION_STATUS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                TRANSACTION_STATUS_KEYWORDS = []
                for row in reader:
                    if 'keyword' in row:
                        TRANSACTION_STATUS_KEYWORDS.append(row['keyword'])
            logger.info(f"Loaded {len(TRANSACTION_STATUS_KEYWORDS)} transaction status keywords")
        else:
            # Create default keywords if file doesn't exist
            TRANSACTION_STATUS_KEYWORDS = ["failed", "unsuccessful", "declined", "rejected", "not processed",
                                         "transaction failed", "payment failed", "insufficient balance",
                                         "could not process", "not successful", "cancelled"]
            logger.info(f"Using default transaction status keywords")

        # Load balance update keywords
        if os.path.exists(BALANCE_UPDATE_FILE):
            with open(BALANCE_UPDATE_FILE, 'r') as f:
                reader = csv.DictReader(f)
                BALANCE_UPDATE_KEYWORDS = []
                for row in reader:
                    if 'keyword' in row:
                        BALANCE_UPDATE_KEYWORDS.append(row['keyword'])
            logger.info(f"Loaded {len(BALANCE_UPDATE_KEYWORDS)} balance update keywords")
        else:
            # Create default keywords if file doesn't exist
            BALANCE_UPDATE_KEYWORDS = ["balance is", "available balance", "current balance", "closing balance",
                                     "bal:", "bal is", "a/c bal", "account balance", "as of",
                                     "updated balance", "balance statement"]
            logger.info(f"Using default balance update keywords")

        # Load bill statement keywords
        if os.path.exists(BILL_STATEMENT_FILE):
            with open(BILL_STATEMENT_FILE, 'r') as f:
                reader = csv.DictReader(f)
                BILL_STATEMENT_KEYWORDS = []
                for row in reader:
                    if 'keyword' in row:
                        BILL_STATEMENT_KEYWORDS.append(row['keyword'])
            logger.info(f"Loaded {len(BILL_STATEMENT_KEYWORDS)} bill statement keywords")
        else:
            # Create default keywords if file doesn't exist
            BILL_STATEMENT_KEYWORDS = ["bill of", "bill amount", "credit card bill", "card bill", "bill generated",
                                     "bill is ready", "bill statement", "bill due", "due on", "minimum due",
                                     "min due", "payment due", "last date", "due date"]
            logger.info(f"Using default bill statement keywords")

        # Load EMI keywords
        if os.path.exists(EMI_KEYWORDS_FILE):
            with open(EMI_KEYWORDS_FILE, 'r') as f:
                reader = csv.DictReader(f)
                EMI_KEYWORDS = []
                for row in reader:
                    if 'keyword' in row:
                        EMI_KEYWORDS.append(row['keyword'])
            logger.info(f"Loaded {len(EMI_KEYWORDS)} EMI keywords")
        else:
            # Create default keywords if file doesn't exist
            EMI_KEYWORDS = ["emi", "equated monthly installment", "loan emi", "emi due", "auto-debit",
                          "auto debit", "loan payment", "will be debited", "pre-emi", "loan installment",
                          "towards loan"]
            logger.info(f"Using default EMI keywords")

    except Exception as e:
        logger.error(f"Error loading data from CSV files: {e}")

# Load data when module is imported
load_data_from_csv()