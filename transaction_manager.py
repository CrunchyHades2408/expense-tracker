import pandas as pd
import os

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
