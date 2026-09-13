import streamlit as st
import hashlib
from backend.pdf_parser import extract_tables_native
from backend.extractor import build_dataframe
from backend.cleaner import clean_transactions
from backend.categorizer import categorize_transactions
from backend.embeddings import embed_transactions
from backend.utils import check_file_size, set_session_df,clear_session
from backend import config
from frontend.components import render_loader, render_error, render_empty_state


def handle_upload():
    uploaded_file = st.file_uploader("Upload bank statement (PDF)", type=["pdf"])

    if uploaded_file is None:
        if st.session_state.get("processed_file_hash"):
            clear_session()

        render_empty_state()
        return

    if not check_file_size(uploaded_file):
        render_error(f"File too large. Max {config.MAX_UPLOAD_MB}MB allowed.")
        return

    pdf_bytes = uploaded_file.getvalue()
    file_hash = hashlib.sha256(pdf_bytes).hexdigest()

    if st.session_state.get("processed_file_hash") == file_hash:
        return

    with render_loader():
        if not pdf_bytes.startswith(b"%PDF"):
            render_error("Uploaded file is not a valid PDF.")
            return

        try:
            rows = extract_tables_native(pdf_bytes)
            df = build_dataframe(rows)
            df = clean_transactions(df)
            df = categorize_transactions(df)
            embed_transactions(df)

        except ValueError as error:
            render_error(f"Could not read transactions from this PDF: {error}")
            return

        set_session_df(df)
        st.session_state["processed_file_hash"] = file_hash

        st.session_state["chat_history"] = []

    st.success(f"Processed {len(df)} transactions.")