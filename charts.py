import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from transaction_manager import load_transactions

def show_spending_chart():
    df = load_transactions()
    if df.empty:
        st.info("Add some transactions to view chart.")
        return

    category_totals = df.groupby("Category")["Amount"].sum()

    if "chart_type" not in st.session_state:
        st.session_state.chart_type = "Pie Chart" 

    chart_type = st.radio("Choose Chart Type", options=["Pie Chart", "Bar Chart"], horizontal=True, key="chart_type")

    if chart_type == "Pie Chart":
        fig, ax = plt.subplots()
        ax.pie(
            category_totals,
            labels=category_totals.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Paired.colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        ax.axis('equal')  
        plt.title("Spending Distribution")
        st.pyplot(fig)

    elif chart_type == "Bar Chart":
        fig, ax = plt.subplots()
        category_totals.plot(kind='bar', ax=ax, color='skyblue')
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        st.pyplot(fig)
