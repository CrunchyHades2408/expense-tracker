import time
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["gemini"]["api_key"])

model = genai.GenerativeModel('gemini-1.5-pro-latest')  

def categorise_using_gemini(description):
    prompt = f"""
    Categorize the following expense into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household, Miscellaneous.

    Expense: {description}
    Respond with only the category name.
    """
    try:
        time.sleep(2)  
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print("Error during Gemini categorization:", e)
        return "Uncategorized"
