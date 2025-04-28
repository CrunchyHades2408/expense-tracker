import cv2
import pytesseract
from expensecategorisation import categorise_using_gemini
from transaction_manager import save_transaction
from datetime import date

def process_bill_image(image_path):
   
    image = cv2.imread(image_path)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    extracted_text = pytesseract.image_to_string(gray)

    transactions = []
    for line in extracted_text.split("\n"):
        if line.strip():
            try:
                parts = line.split()
                transaction_date = date.today() 
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

if __name__ == "__main__":
    image_path = "path_to_bill_image.jpg" 
    process_bill_image(image_path)