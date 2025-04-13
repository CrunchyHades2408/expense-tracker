import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["gemini"]["api_key"])

def categorise_using_gemini(description):
    prompt = f"""
    Categorize the following expense into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household, Micellaneous.

    Expense: {description}
    Respond with only the category name.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    reponse = model.generate_content(prompt)
    return response.text.strip()