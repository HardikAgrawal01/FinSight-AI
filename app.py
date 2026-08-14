import streamlit as st
from frontend.upload import handle_upload
from frontend.dashboard import render_dashboard
from backend.chatbot import render_chatbot
from frontend.components import render_header

st.set_page_config(page_title="FINSIGHT-AI", layout="wide")

render_header()
handle_upload()

if st.session_state.get("transactions_df") is not None:
    tab1, tab2 = st.tabs(["Dashboard", "Chat"])
    with tab1:
        render_dashboard()
    with tab2:
        render_chatbot()