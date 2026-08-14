import streamlit as st


def render_header():
    # top title and tagline shown on every page
    st.title("FINSIGHT-AI")
    st.caption("Upload a bank statement to get instant insights and ask questions about your spending.")


def render_metric_cards(income: float, expense: float, balance: float):
    # three-column summary row for the dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{income:,.2f}")
    col2.metric("Total Expense", f"₹{expense:,.2f}")
    col3.metric("Current Balance", f"₹{balance:,.2f}")


def render_loader(message: str = "Processing your statement..."):
    # spinner wrapper used during PDF parsing/categorization
    return st.spinner(message)


def render_empty_state():
    # shown before any file is uploaded
    st.info("Upload a bank statement PDF to get started.")


def render_error(message: str):
    # consistent error styling across upload/dashboard/chat
    st.error(message)