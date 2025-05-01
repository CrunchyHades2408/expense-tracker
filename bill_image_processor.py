import cv2
import pytesseract
import numpy as np
import re
from expensecategorisation import categorise_using_gemini
from transaction_manager import save_transaction
from datetime import date

# Define keywords of interest to match actual items
VALID_ITEMS = ["coffee", "monster", "maggi"]

def process_bill_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    extracted_text = pytesseract.image_to_string(gray)

    transactions = []
    unique_transactions = set()  # To keep track of already processed transactions

    for line in extracted_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Match pattern like: Maggi Masala 2 Minutes Instant Noodles ₹120
        match = re.search(r'(.+?)\s+₹?(\d+(\.\d{1,2})?)$', line)
        if match:
            description = match.group(1).strip()
            amount = float(match.group(2).strip())

            # Check if the item is one we care about
            if any(item in description.lower() for item in VALID_ITEMS):
                transaction_date = date.today()

                # Create a unique identifier for the transaction (e.g., description + amount)
                transaction_key = (transaction_date, description, amount)

                # Only add if this transaction hasn't been processed yet
                if transaction_key not in unique_transactions:
                    unique_transactions.add(transaction_key)
                    transactions.append((transaction_date, description, amount))

    # Categorize and save
    for transaction_date, description, amount in transactions:
        category = categorise_using_gemini(description)
        save_transaction(transaction_date, description, amount, category)
        print(f"Saved: {transaction_date}, {description}, ₹{amount}, Category: {category}")

    return transactions
