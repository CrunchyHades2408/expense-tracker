import pandas as pd
import os

CSV_FILE = "transactions.csv"

def load_transactions():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Date","Description", "Amount", "Category"])

def save_transactions(date_val, description, amount, category):
    new_entry = pd.DataFrame({
        "Date": [date_val],
        "Description": [description],
         "Amount": [amount],
        "Category": [category]
    })

    df = load_transactions()
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def update_transaction(index, new_data):
    df = load_transactions()
    for key in new_data:
        df.at[index, key] = new_data[key]
    df.to_csv(CSV_FILE, index=False)

def delete_transaction(index):
    df = load_transactions()
    df = df.drop(index=index)
    df.to_csv(CSV_FILE, index=False)