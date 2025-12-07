from dotenv import load_dotenv
load_dotenv()  # load .env if present

import streamlit as st
import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Function to load Gemini model and Get response
# Using gemini-2.5-flash (latest available model)
model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"❌ Error calling Gemini API: {str(e)}")
        return None

# Initialize Streamlit app

st.set_page_config(page_title="Conversational Q&A Chatbot")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
input = st.text_input("Input:", key="input")
submit = st.button("Ask the Question")

if submit and input:
    response = get_gemini_response(input)
    
    if response:
        # Add user query to session chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is:")

        full_response = ""
        for chunk in response:
            st.write(chunk.text)
            full_response += chunk.text
        
        # Add bot response to chat history
        st.session_state['chat_history'].append(("Bot", full_response))

st.subheader("Chat History")


for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")