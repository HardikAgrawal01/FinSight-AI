import streamlit as st
from backup.rag import answer_question
from backend.utils import (
    get_session_df,
    get_chat_history,
    append_chat_message,
)
from frontend.components import render_empty_state


def render_chatbot():
    df = get_session_df()
    if df is None:
        render_empty_state()
        return

    # Display existing chat history first, in chronological order
    # (oldest at top, newest at bottom — standard chat UI convention)
    history = get_chat_history()
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new user input (rendered below history, at the bottom)
    question = st.chat_input("Ask about your transactions...")
    if question:
        append_chat_message("user", question)
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = answer_question(df, question)
            st.markdown(answer)

        append_chat_message("assistant", answer)