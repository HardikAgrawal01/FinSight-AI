import streamlit as st
import pandas as pd
from backend import config


def bytes_to_mb(size_bytes: int) -> float:
    return round(size_bytes / (1024 * 1024), 2)


def check_file_size(uploaded_file) -> bool:
    return uploaded_file.size <= config.MAX_UPLOAD_BYTES


def format_currency(amount: float) -> str:
    return f"₹{amount:,.2f}"


def get_session_df() -> pd.DataFrame | None:
    return st.session_state.get("transactions_df")


def set_session_df(df: pd.DataFrame) -> None:
    st.session_state["transactions_df"] = df


def clear_session() -> None:
    for key in ["transactions_df", "chat_history"]:
        st.session_state.pop(key, None)


def get_chat_history() -> list:
    return st.session_state.setdefault("chat_history", [])


def append_chat_message(role: str, content: str) -> None:
    get_chat_history().append({"role": role, "content": content})