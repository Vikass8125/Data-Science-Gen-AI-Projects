import os
import streamlit as st
from dotenv import load_dotenv
from utils import summarize_pdf

def main():
    st.set_page_config(page_title="PDF Summarizer", page_icon="📄")
    st.write("Summarize your PDF documents easily!")
    st.divider()

    # Load env variables from .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("🔑 OPENAI_API_KEY not found. Please set it in your .env file.")
        return
    os.environ["OPENAI_API_KEY"] = api_key

    pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    submit = st.button("Summarize")

    summary = None
    if submit and pdf_file is not None:
        summary = summarize_pdf(pdf_file)

    st.subheader('Summary:')
    if summary:
        st.write(summary)
    else:
        st.write("Please upload a PDF and click ‘Summarize’.")

if __name__ == "__main__":
    main()
