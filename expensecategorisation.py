import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt # type: ignore
import google.generativeai as genai
from datetime import date

# === Gemini API Setup ===
genai.configure(api_key=st.secrets["gemini"]["api_key"])

def categorize_using_gemini(description):
    prompt = f"""
    Categorize the following expense into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household.

    Expense: {description}
    Respond only with the category name.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# === File Handling ===
CSV_FILE = "transactions.csv"

def save_transaction(date_val, description, amount, category):
    data = {
        "Date": [date_val],
        "Description": [description],
        "Amount": [amount],
        "Category": [category]
    }

    new_entry = pd.DataFrame(data)

    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry

    updated.to_csv(CSV_FILE, index=False)

# === Visualization ===
def show_spending_chart():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        category_totals = df.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()
        category_totals.plot(kind='bar', ax=ax, color='skyblue')
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        st.pyplot(fig)
    else:
        st.info("Add some transactions to view chart.")

# === Streamlit UI ===
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💸")
st.title("💸 Smart Expense Tracker")

st.subheader("Add New Expense")

col1, col2 = st.columns(2)
with col1:
    date_val = st.date_input("📅 Date", value=date.today())
with col2:
    amount = st.number_input("💵 Amount", min_value=0, step=10)

description = st.text_input("📝 Expense Description")

if st.button("Categorize and Save"):
    if description and amount > 0:
        category = categorize_using_gemini(description)
        save_transaction(date_val, description, amount, category)
        st.success(f"Saved! Category: **{category}**")
    else:
        st.warning("Please enter a valid description and amount.")

st.markdown("---")
st.subheader("📋 All Transactions")

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions recorded yet.")

st.markdown("---")
st.subheader("📊 Spending Overview")
show_spending_chart()
