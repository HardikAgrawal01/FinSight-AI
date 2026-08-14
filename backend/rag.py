import pandas as pd
from backend.llm import ask_llm
from backend.embeddings import query_similar

SAFE_BUILTINS = {
    "len": len, "sum": sum, "min": min, "max": max,
    "round": round, "abs": abs, "sorted": sorted,
    "list": list, "dict": dict, "str": str, "int": int, "float": float,
}


def generate_pandas_code(question: str, df_columns: list[str], df: pd.DataFrame) -> str:
    categories = df["category"].dropna().unique().tolist()
    prompt = (
        f"The dataframe 'df' has columns: {df_columns}. "
        f"A dictionary named 'statement_info' is also available. "
        f"It contains: opening_balance, closing_balance, statement_start, "
        f"statement_end, total_debit, total_credit, transaction_count. "
        f"For questions asking these values, use statement_info directly. "
        f"The 'category' column only contains: {categories}. "
        f"If the question is about a general spending type (food, shopping, transport, "
        f"bills, etc.) and a matching category exists in the list above, filter using "
        f"the category column instead of searching description text. Only search "
        f"description text for specific merchant names not covered by a category. "
        f"For merchant/keyword text search, use df['description'].str.contains(keyword, "
        f"case=False, na=False) directly — do NOT use 'keyword in df[...].values' or any "
        f"exact-match guard condition. "
        f"Write ONE line of pandas code (no explanation, no imports, no markdown) "
        f"that answers: '{question}'. Assign the result to a variable named result. "
        f"If truly unanswerable, set result = None."
    )
    code = ask_llm(prompt, temperature=0.0)
    return code.strip().strip("`")


def run_pandas_query(df: pd.DataFrame, question: str):
    df = df.sort_values("date")

    statement_info = {
        "opening_balance": df.iloc[0]["balance"] - df.iloc[0]["credit"] + df.iloc[0]["debit"],
        "closing_balance": df.iloc[-1]["balance"],
        "statement_start": df.iloc[0]["date"],
        "statement_end": df.iloc[-1]["date"],
        "total_debit": df["debit"].sum(),
        "total_credit": df["credit"].sum(),
        "transaction_count": len(df),
    }

    code = generate_pandas_code(question, list(df.columns), df)
    print("generated code:", code)

    local_vars = {"df": df, "pd": pd, "statement_info": statement_info}
    try:
        exec(code, {"__builtins__": SAFE_BUILTINS}, local_vars)
        return local_vars.get("result")
    except Exception as e:
        print("exec failed:", e)
        return None


def answer_question(df: pd.DataFrame, question: str) -> str:
    pandas_result = run_pandas_query(df, question)

    if pandas_result is not None:
        is_multi_row = isinstance(pandas_result, (pd.DataFrame, pd.Series)) and len(pandas_result) > 1

        if is_multi_row:
            result_text = pandas_result.to_string()
            context = (
                f"User question: {question}\n"
                f"Exact computed result:\n{result_text}\n"
                f"Report EVERY row shown above, in Indian Rupees (₹). "
                f"Format as a markdown bullet list, one transaction per line, "
                f"with a blank line between each bullet. Do not recalculate."
            )
        else:
            result_text = str(pandas_result)
            context = (
                f"User question: {question}\n"
                f"Exact computed result: {result_text}\n"
                f"Report this single value in one short plain-language sentence. "
                f"Use ₹ only if it represents money, not for counts. Do not recalculate."
            )
        return ask_llm(context)

    semantic_result = query_similar(question)
    if not semantic_result:
        return "I couldn't find any matching transactions for this."

    matches_text = "\n\n".join(
        f"- {m['date']}: {m['description']} — ₹{m.get('debit', 0)}"
        for m in semantic_result
    )
    return (
        f"I don't have a verified total for this, but here are the matching "
        f"transactions:\n\n{matches_text}"
    )