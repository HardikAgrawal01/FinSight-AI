import pandas as pd
import plotly.express as px

def total_income(df: pd.DataFrame) -> float:
    return df["credit"].sum()

def total_expense(df: pd.DataFrame) -> float:
    return df["debit"].sum()

def net_balance(df: pd.DataFrame) -> float:
    return df.sort_values("date")["balance"].iloc[-1]

def spend_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("category")["debit"].sum().sort_values(ascending=False).reset_index())

def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()

    temp["month"] = (temp["date"].dt.to_period("M").astype(str))

    return (
        temp.groupby("month")[["credit", "debit"]]
        .sum()
        .reset_index()
    )


def top_merchants(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return (
        df.groupby("description")["debit"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


# ---------------------------
# PLOTLY CHARTS
# ---------------------------


def category_pie_chart(df):

    data = spend_by_category(df)

    fig = px.pie(
        data,
        names="category",
        values="debit",
        hole=0.45,
        title="Spending by Category",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    return fig



def income_expense_chart(df):

    data = pd.DataFrame({
        "Type": [
            "Income",
            "Expense"
        ],
        "Amount": [
            total_income(df),
            total_expense(df)
        ]
    })

    fig = px.bar(
        data,
        x="Type",
        y="Amount",
        text="Amount",
        title="Income vs Expense",
        color="Type",
        color_discrete_map={
            "Income": "#00C853",      # Green
            "Expense": "#FF3D00"      # Red
        }
    )

    return fig



def monthly_trend_chart(df):

    data = monthly_trend(df)

    fig = px.line(
        data,
        x="month",
        y=["credit", "debit"],
        markers=True,
        title="Monthly Cash Flow",
        color_discrete_sequence=[
            "#00C853",
            "#FF3D00"
        ]
    )

    return fig



def balance_chart(df):

    data = df.sort_values("date")

    fig = px.area(
        data,
        x="date",
        y="balance",
        title="Balance Trend",
        color_discrete_sequence=["#27C2CD"]
    )

    return fig



def top_merchants_chart(df):

    data = top_merchants(df, 10)

    fig = px.bar(
        data,
        x="debit",
        y="description",
        orientation="h",
        title="Top Merchants",
        text="debit",
        color="debit",
        color_continuous_scale="Turbo"
    )

    return fig