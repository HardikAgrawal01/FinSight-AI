import streamlit as st
from backend.pdf_parser import extract_tables_native
from backend.extractor import build_dataframe
from backend.cleaner import clean_transactions
from backend.categorizer import categorize_transactions
from backend.embeddings import embed_transactions
from backend.utils import check_file_size, set_session_df
from backend import config
from frontend.components import render_loader, render_error, render_empty_state


def handle_upload():
    # main upload flow: validate, extract table, clean, categorize, embed
    uploaded_file = st.file_uploader("Upload bank statement (PDF)", type=["pdf"])

    if uploaded_file is None:
        render_empty_state()
        return

    if not check_file_size(uploaded_file):
        render_error(f"File too large. Max {config.MAX_UPLOAD_MB}MB allowed.")
        return

    with render_loader():
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()

        if not pdf_bytes.startswith(b"%PDF"):
            render_error("Uploaded file is not a valid PDF.")
            return

        try:
            rows = extract_tables_native(pdf_bytes)
            df = build_dataframe(rows)
        except ValueError as e:
            render_error(f"Could not read transactions from this PDF: {e}")
            return

        df = clean_transactions(df)
        df = categorize_transactions(df)
        embed_transactions(df)

        set_session_df(df)
    rows = extract_tables_native(pdf_bytes)

    st.success(f"Processed {len(df)} transactions.")