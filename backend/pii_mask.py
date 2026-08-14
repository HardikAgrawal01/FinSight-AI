import re
from backend import config

TABLE_HEADER_PATTERN = re.compile(
    r"(date).{0,40}(narration|description|particulars).{0,40}(balance)",
    re.IGNORECASE,
)

PHONE_PATTERN = re.compile(r"\b\d{10}\b")
UPI_PATTERN = re.compile(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b")
LONG_NUMBER_PATTERN = re.compile(r"\b\d{9,18}\b")

def scrub_narration(text: str) -> str:
    text = PHONE_PATTERN.sub("[PHONE]", text)
    text = UPI_PATTERN.sub("[UPI_ID]", text)
    text = LONG_NUMBER_PATTERN.sub("[ACC_NO]", text)
    return text