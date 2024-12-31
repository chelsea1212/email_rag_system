import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import pandas

def initialize_gemini():
    """Initialize the Gemini API with the API key."""
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyA0lR8habHP6Zv38a66dF5QikrYBhz-FnI')
    genai.configure(api_key=GEMINI_API_KEY)


def generate_gemini_response(prompt):
    """Generate response using Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


def search_emails(query, data):
    """Search through emails and generate response using Gemini."""
    keywords = query.lower().split()
    relevant_rows = []

    # Search for keywords in the email body
    for _, row in data.iterrows():
        body = str(row["Body"]).lower()
        if any(keyword in body for keyword in keywords):
            relevant_rows.append(row)

    if not relevant_rows:
        return "No relevant emails found."

    prompt = f"""Based on the following email data, please answer this query: {query}

Relevant emails:
"""
    for row in relevant_rows:
        prompt += f"\nSubject: {row['Subject']}\nBody: {row['Body']}\n---"

    return generate_gemini_response(prompt)


def main():
    st.set_page_config(page_title="Email Search Assistant", page_icon="📧")

    # Initialize Gemini
    initialize_gemini()

    # Application title
    st.title(" Email Search Assistant")

    try:
        # Load the email data directly
        email_data = pd.read_csv("data/emails.csv")  # Make sure this path matches your CSV file location
        st.success(f"Loaded {len(email_data)} emails successfully!")

        # Search interface
        st.subheader("Search Emails")
        query = st.text_input("Enter your search query:")

        if st.button("Search"):
            if query:
                with st.spinner('Searching emails and generating response...'):
                    result = search_emails(query, email_data)
                    st.subheader("Search Results")
                    st.write(result)
            else:
                st.warning("Please enter a search query.")

    except Exception as e:
        st.error(f"Error loading emails.csv: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("Powered by Google Gemini AI")


if __name__ == "__main__":
    main()