import os
from pathlib import Path

MAX_UPLOAD_MB = 1
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent.parent
# CHROMA_DB_PATH = BASE_DIR / "data" / "chroma_db"
CHROMA_COLLECTION_NAME = "transactions"

GROQ_MODEL_NAME = "openai/gpt-oss-120b"
# GEMINI_MODEL_NAME = "gemini-3.6-flash"
# GEMINI_MODEL_NAME = "gemini-3.6-flash"
# ENV_GEMINI_API_KEY = "GEMINI_API_KEY"

LLM_TEMPERATURE = 0.2
LLM_MAX_RETRIES = 2

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


ENV_GROQ_API_KEY = "GROQ_API_KEY"
ENV_GEMINI_API_KEY = "GEMINI_API_KEY"


KOTAK_COLUMN_MAP = {
    "date": "Date",
    "description": "Description",
    "debit": "Withdrawal (Dr.)",
    "credit": "Deposit (Cr.)",
    "balance": "Balance",
}

CATEGORY_KEYWORDS = {
    "Food & Dining": [
        "swiggy", "zomato", "restaurant", "cafe", "food", "dominos",
        "pizza", "mcdonald", "kfc", "starbucks", "eatery", "dhaba",
        "bakery", "biryani", "food court",
    ],
    "Groceries": [
        "bigbasket", "grocery", "supermarket", "dmart", "reliance fresh",
        "more supermarket", "grofers", "blinkit", "zepto", "instamart",
        "spencers", "kirana",
    ],
    "Transport": [
        "uber", "ola", "fuel", "petrol", "diesel", "metro", "irctc",
        "rapido", "indian oil", "bharat petroleum", "hpcl", "toll",
        "fastag", "parking", "bus", "cab",
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "nykaa", "meesho",
        "snapdeal", "shopclues", "tatacliq", "reliance digital",
        "croma", "decathlon",
    ],
    "Bills & Utilities": [
        "electricity", "recharge", "broadband", "dth", "airtel",
        "jio", "vodafone", "vi ", "wifi", "gas bill", "water bill",
        "postpaid", "prepaid", "internet bill", "mobile bill",
    ],
    "Rent": ["rent", "landlord", "house rent", "rental"],
    "Salary/Income": [
        "salary", "credited", "neft cr", "imps cr", "stipend",
        "bonus", "reimbursement", "payroll", "income",
    ],
    "Entertainment": [
        "netflix", "spotify", "prime video", "hotstar", "sonyliv",
        "zee5", "bookmyshow", "pvr", "inox", "youtube premium",
        "gaana", "jiocinema",
    ],
    "Transfers": [
        "upi", "neft", "imps", "rtgs", "gpay", "phonepe", "paytm",
        "cred", "bhim", "p2p",
    ],
    "Healthcare": [
        "pharmacy", "hospital", "clinic", "apollo", "medplus",
        "1mg", "practo", "diagnostic", "medical", "doctor",
    ],
    "Investments": [
        "zerodha", "groww", "upstox", "mutual fund", "sip",
        "stocks", "demat", "coin", "kite",
    ],
    "Insurance": ["premium", "lic", "policybazaar", "insurance"],
    "Education": [
        "udemy", "coursera", "tuition", "school fee", "college fee",
        "byjus", "unacademy", "exam fee",
    ],
    "EMI/Loan": ["emi", "loan", "installment", "bajaj finserv"],
    "ATM/Cash": ["atm", "cash withdrawal", "cash wdl"],
}
DEFAULT_CATEGORY = "Uncategorized"

PII_FIELD_LABELS = ["account no", "a/c no", "ifsc", "name", "address", "customer id"]