import streamlit as st
from datetime import date
from transaction_manager import import_upi_history_file, load_transactions
from charts import show_spending_chart
from expensecategorisation import categorise_using_gemini


# === Streamlit UI Setup ===
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💸")
st.title("💸 Smart Expense Tracker")

# Section for uploading UPI transaction file
st.markdown("---")
st.subheader("📥 Import UPI Transaction History")
uploaded_file = st.file_uploader("Upload UPI transaction file (CSV or Excel)", type=["csv", "xls", "xlsx"], key="upi_upload")

if uploaded_file is not None:
    success, message = import_upi_history_file(uploaded_file)
    if success:
        st.success(message)
        st.experimental_rerun()  # Reload the app to show updated data
    else:
        st.error(message)

# === Add New Expense Section ===
st.markdown("---")
st.subheader("📝 Add New Expense")

# Date and amount input fields
col1, col2 = st.columns(2)
with col1:
    date_val = st.date_input("📅 Date", value=date.today())
with col2:
    amount = st.number_input("💵 Amount", min_value=0, step=10)

description = st.text_input("📝 Expense Description")

if st.button("Categorize and Save"):
    if description and amount > 0:
        category = categorize_using_gemini(description)  # Categorize using Gemini
        # Save to CSV or database (you can call save_transaction from transaction_manager)
        save_transaction(date_val, description, amount, category)  # Assuming you have this method
        st.success(f"Saved! Category: **{category}**")
    else:
        st.warning("Please enter a valid description and amount.")

# === Display All Transactions ===
st.markdown("---")
st.subheader("📋 All Transactions")
df = load_transactions()

if df.empty:
    st.info("No transactions recorded yet.")
else:
    st.dataframe(df, use_container_width=True)

# === Spending Overview: Chart Section ===
st.markdown("---")
st.subheader("📊 Spending Overview")
show_spending_chart()  # This function should show the spending chart
