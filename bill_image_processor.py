import cv2
import pytesseract
import numpy as np
from expensecategorisation import categorise_using_gemini
from transaction_manager import save_transaction
from datetime import date

def process_bill_image(uploaded_file):
    # Read the uploaded file as a byte stream
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    
    # Decode the byte stream into an image
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Extract text using Tesseract OCR
    extracted_text = pytesseract.image_to_string(gray)

    transactions = []
    for line in extracted_text.split("\n"):
        if line.strip():
            try:
                parts = line.split()
                transaction_date = date.today()  # Default to today's date
                description = " ".join(parts[:-1])
                amount = float(parts[-1])
                transactions.append((transaction_date, description, amount))
            except ValueError:
                continue

    # Categorize and save transactions
    for transaction_date, description, amount in transactions:
        category = categorise_using_gemini(description)
        save_transaction(transaction_date, description, amount, category)
        print(f"Saved: {transaction_date}, {description}, ₹{amount}, Category: {category}")

    return transactions