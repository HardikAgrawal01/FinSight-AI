import pandas as pd
from dataclasses import dataclass
from datetime import date

EXPECTED_COLUMNS = ["date", "description", "debit", "credit", "balance", "category"]

DEDUPE_KEYS = ["date", "description", "debit", "credit", "balance"]


@dataclass
class Transaction:
    date: date
    description: str
    debit: float
    credit: float
    balance: float
    category: str = "Uncategorized"

def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in transaction data: {missing}")

    df = df[EXPECTED_COLUMNS].copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["debit"] = pd.to_numeric(df["debit"], errors="coerce").fillna(0.0)
    df["credit"] = pd.to_numeric(df["credit"], errors="coerce").fillna(0.0)
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce")
    df["description"] = df["description"].astype(str).str.strip()
    df["category"] = df["category"].fillna("Uncategorized")

    invalid_rows = df["date"].isna().sum()
    if invalid_rows:
        df = df[df["date"].notna()].reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid transaction rows found after cleaning.")

    return df