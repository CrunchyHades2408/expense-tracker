import pandas as pd
import os
from expensecategorisation import categorise_using_gemini

CSV_FILE = "transactions.csv"

def load_transactions():
    # Load existing transaction history
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])

def save_transaction(date, description, amount, category):
    # Append new transaction to the CSV file
    new_transaction = pd.DataFrame([{
        "Date": date,
        "Description": description,
        "Amount": amount,
        "Category": category
    }])

    # Load existing transactions and append the new one
    df = load_transactions()
    df = pd.concat([df, new_transaction], ignore_index=True)

    # Save the updated DataFrame back to CSV
    df.to_csv(CSV_FILE, index=False)

def import_upi_history_file(uploaded_file):
    # Parse and categorize UPI transactions
    if uploaded_file is not None:
        try:
            # Parse the uploaded UPI file (CSV or Excel)
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
            else:
                return False, "Unsupported file type. Please upload a CSV or Excel file."

            # Try to infer relevant columns (Date, Description, Amount)
            date_col = next((col for col in df.columns if "date" in col.lower()), None)
            desc_col = next((col for col in df.columns if "description" in col.lower() or "narration" in col.lower()), None)
            amount_col = next((col for col in df.columns if "amount" in col.lower()), None)

            if not all([date_col, desc_col, amount_col]):
                return False, "Required columns not found (Date, Description, Amount)."

            # Rename columns for consistency
            df = df[[date_col, desc_col, amount_col]]
            df.columns = ["Date", "Description", "Amount"]

            # Categorize using Gemini
            df["Category"] = df["Description"].apply(categorise_using_gemini)

            # Merge with existing transaction history
            existing_df = load_transactions()
            updated_df = pd.concat([existing_df, df], ignore_index=True)

            # Save the updated transaction history
            updated_df.to_csv(CSV_FILE, index=False)
            return True, "UPI transactions imported and categorized successfully."

        except Exception as e:
            return False, f"Error processing file: {e}"

    return False, "No file uploaded."
