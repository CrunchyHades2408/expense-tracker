import pandas as pd
import os
from expensecategorisation import categorise_using_gemini

CSV_FILE = "transactions.csv"

def load_transactions():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Description", "Amount", "Category"])

def save_transaction(date, description, amount, category):
    new_transaction = pd.DataFrame([{
        "Date": date,
        "Description": description,
        "Amount": amount,
        "Category": category
    }])
    df = load_transactions()
    df = pd.concat([df, new_transaction], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def import_upi_history_file(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
            else:
                return False, "Unsupported file type. Please upload a CSV or Excel file."

            date_col = next((col for col in df.columns if "date" in col.lower()), None)
            desc_col = next((col for col in df.columns if "description" in col.lower() or "narration" in col.lower()), None)
            amount_col = next((col for col in df.columns if "amount" in col.lower()), None)

            if not all([date_col, desc_col, amount_col]):
                return False, "Required columns not found (Date, Description, Amount)."

            df = df[[date_col, desc_col, amount_col]]
            df.columns = ["Date", "Description", "Amount"]
            df["Category"] = df["Description"].apply(categorise_using_gemini)

            existing_df = load_transactions()
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv(CSV_FILE, index=False)

            return True, "UPI transactions imported and categorized successfully."

        except Exception as e:
            return False, f"Error processing file: {e}"

    return False, "No file uploaded."
