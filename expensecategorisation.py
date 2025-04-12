import streamlit as st
import google.generativeai as genai


genai.configure(api_key=st.secrets["gemini"]["api_key"])

def predict_category(description):
    prompt = f"""
    Categorize the following expense description into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household.

    Description: '{description}'

    Respond with only the category name.
    """

    try:
        model = genai.GenerativeModel("gemini-pro") 
        response = model.generate_content(prompt)
        category = response.text.strip()  
        return category
    except Exception as e:
        return f"Error: {e}"
st.set_page_config(page_title="Smart Expense Categorizer", page_icon="💸")

st.title("💸 Smart Expense Categorizer (AI-Powered)")
st.markdown("Enter any **expense description**, and AI will categorize it for you!")

description = st.text_input("📝 Expense Description:")

if description:
    category = predict_category(description)
    st.success(f"📂 Predicted Category: **{category}**")
