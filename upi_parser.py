import pandas as pd
import google.generativeai as genai
import streamlit as st

# === Configure Gemini API with Streamlit's secrets ===
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# === Gemini Categorization Function ===
def categorise_using_gemini(description):
    prompt = f"""
    Categorize the following expense into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household, Others.

    Expense: {description}
    Respond only with the category name.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# === Read and Process UPI Transactions ===
def read_and_categorize_transactions(uploaded_file):
    # Read file from uploaded file
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a CSV or Excel file.")
                return None

            # Try to infer columns
            date_col = next((col for col in df.columns if "date" in col.lower()), None)
            desc_col = next((col for col in df.columns if "description" in col.lower() or "narration" in col.lower()), None)
            amount_col = next((col for col in df.columns if "amount" in col.lower()), None)

            if not all([date_col, desc_col, amount_col]):
                st.error("Required columns not found (Date, Description, Amount). Please check your file format.")
                return None

            # Rename for consistency
            df = df[[date_col, desc_col, amount_col]]
            df.columns = ["Date", "Description", "Amount"]

            # Categorize each transaction using Gemini
            st.info("Categorizing transactions... Please wait.")
            df["Category"] = df["Description"].apply(categorize_using_gemini)

            return df
        except
