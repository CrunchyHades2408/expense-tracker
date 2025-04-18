import streamlit as st
from datetime import date
from transaction_manager import import_upi_history_file, load_transactions, save_transaction, delete_transaction
from charts import show_spending_chart
from expensecategorisation import categorise_using_gemini

# === Streamlit UI Setup ===
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💸")
st.title("💸 Smart Expense Tracker")

# Optional rerun fix if st.experimental_rerun() crashes
if 'deleted' in st.session_state:
    del st.session_state['deleted']
    st.experimental_rerun()

# Section for uploading UPI transaction file
st.markdown("---")
st.subheader("📥 Import UPI Transaction History")
uploaded_file = st.file_uploader("Upload UPI transaction file (CSV or Excel)", type=["csv", "xls", "xlsx"], key="upi_upload")

if uploaded_file is not None:
    success, message = import_upi_history_file(uploaded_file)
    if success:
        st.session_state.uploaded_file = uploaded_file  # Save uploaded file in session state
        st.success(message)
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
        category = categorise_using_gemini(description)  # Categorize using Gemini
        save_transaction(date_val, description, amount, category)  # Save the new expense
        st.success(f"Saved! Category: **{category}**")
        st.experimental_rerun()
    else:
        st.warning("Please enter a valid description and amount.")

# === Display All Transactions with Delete ===
st.markdown("---")
st.subheader("📋 All Transactions")
df = load_transactions()

if df.empty:
    st.info("No transactions recorded yet.")
else:
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
        with col1:
            st.write(row['Date'])
        with col2:
            st.write(row['Description'])
        with col3:
            st.write(f"₹{row['Amount']}")
        with col4:
            st.write(row['Category'])
        with col5:
            if st.button("🗑️", key=f"delete_{i}"):
                success, msg = delete_transaction(i)
                if success:
                    st.success(msg)
                    st.session_state['deleted'] = True  # Trigger rerun safely
                    st.stop()
                else:
                    st.error(msg)

# === Spending Overview: Chart Section ===
st.markdown("---")
st.subheader("📊 Spending Overview")
show_spending_chart()  # This function should show the spending chart
