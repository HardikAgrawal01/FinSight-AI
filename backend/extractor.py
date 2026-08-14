import pandas as pd
from backend.pii_mask import scrub_narration
from backend import config

# FOR KOTAK
def parse_amount(value) -> float:
    if not value or str(value).strip() in ("", "-"):
        return 0.0
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None  # signals "this wasn't actually a number row"

def find_header_row(rows: list) -> int | None:
    for i, row in enumerate(rows):
        cells = [c or "" for c in row]
        if any("date" in c.lower() for c in cells) and any("balance" in c.lower() for c in cells):
            return i
    return None


def map_columns(header_row: list) -> dict:
    mapping = {}
    for field, label in config.KOTAK_COLUMN_MAP.items():
        for idx, cell in enumerate(header_row):
            if cell and label.lower() in cell.lower():
                mapping[field] = idx
                break
    return mapping

LEGEND_EXACT_PREFIXES = [
    "netcard", "os -", "ot -", "pb -", "pci/pcd", "rtgs -",
    "upi -", "visaccpay", "vmt -", "wb -", "int. pd.",
    "sweep transfer to -", "sweep transfer from -", "opening balance",
]

def is_legend_row(row: list) -> bool:
    # legend rows can have their text in any column depending on page layout
    combined = " ".join(str(c or "") for c in row).lower().strip()
    return any(combined.startswith(prefix) or prefix in combined for prefix in LEGEND_EXACT_PREFIXES)


def build_dataframe(rows: list) -> pd.DataFrame:
    header_idx = find_header_row(rows)
    if header_idx is None:
        raise ValueError("Could not find transaction table header")

    col_map = map_columns(rows[header_idx])
    records = []
    skipped = {"header": 0, "legend": 0, "invalid_date": 0, "invalid_amount": 0}

    for row in rows[header_idx + 1:]:
        if is_header_row(row):
            skipped["header"] += 1
            continue

        if is_legend_row(row):
            skipped["legend"] += 1
            continue

        date_val = safe_get(row, col_map.get("date"))
        if not is_valid_date(date_val):
            skipped["invalid_date"] += 1
            continue

        desc_val = str(safe_get(row, col_map.get("description")) or "")
        debit = parse_amount(safe_get(row, col_map.get("debit")))
        credit = parse_amount(safe_get(row, col_map.get("credit")))
        balance = parse_amount(safe_get(row, col_map.get("balance")))

        if debit is None or credit is None or balance is None:
            skipped["invalid_amount"] += 1
            continue

        records.append({
            "date": str(date_val).strip(),
            "description": scrub_narration(desc_val.strip()),
            "debit": debit,
            "credit": credit,
            "balance": balance,
        })

    
    df = pd.DataFrame(records)
    df["category"] = None
    return df

def safe_get(row: list, idx: int | None):
    if idx is None or idx >= len(row):
        return None
    return row[idx]

def is_valid_date(value) -> bool:
    return bool(value) and str(value).strip() not in ("", "-")


def is_header_row(row: list) -> bool:
    cells = [str(c or "").lower() for c in row]
    return any("date" in c for c in cells) and any("balance" in c for c in cells)
