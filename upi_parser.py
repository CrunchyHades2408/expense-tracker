import pandas as pd
import google.generativeai as genai
import streamlit as st

# === Configure Gemini API with Streamlit's secrets ===
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# === Gemini Categorization Function ===
def categorize_using_gemini(description):
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
def read_and_categorize_transactions(file_path):
    # Read file
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Use CSV or Excel.")

    # Try to infer columns
    date_col = next((col for col in df.columns if "date" in col.lower()), None)
    desc_col = next((col for col in df.columns if "description" in col.lower() or "narration" in col.lower()), None)
    amount_col = next((col for col in df.columns if "amount" in col.lower()), None)

    if not all([date_col, desc_col, amount_col]):
        raise ValueError("Required columns not found (Date, Description, Amount)")

    # Rename for consistency
    df = df[[date_col, desc_col, amount_col]]
    df.columns = ["Date", "Description", "Amount"]

    # Categorize each transaction using Gemini
    print("Categorizing transactions...")
    df["Category"] = df["Description"].apply(categorize_using_gemini)

    return df

# === Example Usage ===
if __name__ == "__main__":
    file_path = "upi_transactions.xlsx"  # Replace with your file path
    categorized_df = read_and_categorize_transactions(file_path)
    print(categorized_df.head())

    # Optionally save to CSV
    categorized_df.to_csv("categorized_transactions.csv", index=False)
    print("Saved as categorized_transactions.csv")
