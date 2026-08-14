import pandas as pd
from backend import config
from backend.llm import ask_llm


def extract_merchant(description: str) -> str:
    parts = description.split("/")
    if len(parts) >= 2 and parts[0].strip().upper() == "UPI":
        return parts[1].strip()
    return description

def rule_based_category(description: str) -> str | None:
    merchant = extract_merchant(description).lower()
    for category, keywords in config.CATEGORY_KEYWORDS.items():
        if any(kw in merchant for kw in keywords):
            return category
    return None

def llm_categorize_batch(descriptions: list[str]) -> list[str]:
    categories = list(config.CATEGORY_KEYWORDS.keys())
    numbered = "\n".join(f"{i}: {d}" for i, d in enumerate(descriptions))
    prompt = (
        f"Classify each numbered transaction into exactly one category from this list: "
        f"{categories}. Reply with exactly one line per transaction, in the format "
        f"'NUMBER: CATEGORY', same numbering as given, nothing else.\n\n{numbered}"
    )
    response = ask_llm(prompt).strip().splitlines()

    result_map = {}
    for line in response:
        if ":" not in line:
            continue
        idx_str, cat = line.split(":", 1)
        idx_str, cat = idx_str.strip(), cat.strip()
        if idx_str.isdigit() and cat in categories:
            result_map[int(idx_str)] = cat

    return [result_map.get(i, config.DEFAULT_CATEGORY) for i in range(len(descriptions))]


def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    categories = []
    unmatched_idx = []
    unmatched_desc = []

    for i, desc in enumerate(df["description"]):
        cat = rule_based_category(desc)
        categories.append(cat)
        if cat is None:
            unmatched_idx.append(i)
            unmatched_desc.append(desc)

    if unmatched_desc:
        llm_results = llm_categorize_batch(unmatched_desc)
        for idx, cat in zip(unmatched_idx, llm_results):
            categories[idx] = cat

    df["category"] = categories
    return df