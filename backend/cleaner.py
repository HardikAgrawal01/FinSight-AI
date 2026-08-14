import pandas as pd
from backend.schemas import validate_schema, DEDUPE_KEYS


def dedupe_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # drop only exact repeats across date+description+debit+credit+balance
    return df.drop_duplicates(subset=DEDUPE_KEYS, keep="first")


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    # removes rows where extraction failed to find any amount at all
    return df[(df["debit"] != 0) | (df["credit"] != 0)]


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # full cleaning pass: validate schema, dedupe, drop junk rows
    df = validate_schema(df)
    df = dedupe_transactions(df)
    df = drop_empty_rows(df)
    df = df.sort_values("date").reset_index(drop=True)
    return df