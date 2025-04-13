
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Function to predict the expense category
def predict_category(description):
    prompt = f"""
    Categorize the following expense description into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household.

    Description: '{description}'

    Respond with only the category name.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest") 
        response = model.generate_content(prompt)
        category = response.text.strip()  
        return category
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="BudgetFlow", page_icon="💸")

st.title("💸 Expense Categorizer")
st.markdown("Enter your **expense description** and **amount**:")

# Input fields
description = st.text_input("📝 Expense Description:")
amount = st.number_input("💰 Expense Amount (in ₹):", min_value=0.0, step=0.5)

# Show prediction when description and amount are entered
if description and amount > 0:
    category = predict_category(description)
    st.success(f"📂 Category: **{category}**")
    st.info(f"💸 Amount: ₹{amount}")

