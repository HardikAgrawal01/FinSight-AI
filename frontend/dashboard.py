import streamlit as st

from backend.dashboard import (
    total_income,
    total_expense,
    net_balance,
    category_pie_chart,
    income_expense_chart,
    monthly_trend_chart,
    balance_chart,
    top_merchants_chart,
)

from backend.utils import get_session_df
from frontend.components import (
    render_metric_cards,
    render_empty_state
)


def render_dashboard():

    df = get_session_df()

    if df is None:
        render_empty_state()
        return


    st.title("💰 FinSight AI Dashboard")


    # -------------------
    # KPI CARDS
    # -------------------

    render_metric_cards(
        income=total_income(df),
        expense=total_expense(df),
        balance=net_balance(df),
    )


    st.divider()


    # -------------------
    # ROW 1
    # -------------------

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            category_pie_chart(df),
            width="stretch"
        )

    with col2:
        st.plotly_chart(
            income_expense_chart(df),
            width="stretch"
        )


    # -------------------
    # ROW 2
    # -------------------

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            monthly_trend_chart(df),
            width="stretch"
        )

    with col2:
        st.plotly_chart(
            balance_chart(df),
            width="stretch"
        )


    # -------------------
    # ROW 3
    # -------------------

    st.plotly_chart(
        top_merchants_chart(df),
        width="stretch"
    )