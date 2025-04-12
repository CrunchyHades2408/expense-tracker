import streamlit as st
import openai

# 🔐 Securely load API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# 🚀 Predict category using OpenAI API
def predict_category(description):
    prompt = f"""
    Categorize the following expense description into one of these categories:
    Food & Drink, Transport, Shopping, Entertainment, Utilities, Healthcare, Travel, Education, Household.

    Description: '{description}'

    Respond with only the category name.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=20
        )
        category = response['choices'][0]['message']['content'].strip()
        return category
    except Exception as e:
        return f"Error: {e}"

# 🌐 Streamlit App UI
st.set_page_config(page_title="Smart Expense Categorizer", page_icon="💸")

st.title("💸 Smart Expense Categorizer (AI-Powered)")
st.markdown("Enter any **expense description**, and AI will categorize it for you!")

description = st.text_input("📝 Expense Description:")

if description:
    category = predict_category(description)
    st.success(f"📂 Predicted Category: **{category}**")
