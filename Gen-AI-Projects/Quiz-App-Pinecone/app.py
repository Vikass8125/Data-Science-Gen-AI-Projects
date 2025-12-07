# app.py
import streamlit as st
import os
from llm_engine import (
    load_and_split_pdf_directory,
    create_or_recreate_index,
    ask_with_index
)

# Page configuration
st.set_page_config(
    page_title="📚 Quiz App with Pinecone",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 Quiz App — Chat with PDFs from Documents")

# Initialize session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "index_loaded" not in st.session_state:
    st.session_state.index_loaded = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    doc_directory = st.text_input(
        "📁 Document Directory",
        value="documents/",
        help="Path to folder containing PDFs"
    )
    
    chunk_size = st.slider(
        "Chunk Size",
        min_value=200,
        max_value=2000,
        value=800,
        step=100,
        help="Size of text chunks for splitting"
    )
    
    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=0,
        max_value=500,
        value=50,
        step=10,
        help="Overlap between consecutive chunks"
    )
    
    k_results = st.slider(
        "Top K Results",
        min_value=1,
        max_value=10,
        value=4,
        help="Number of similar documents to retrieve"
    )
    
    st.divider()
    
    if st.button("🔄 Load/Reload Documents", key="load_docs", use_container_width=True):
        with st.spinner("Loading and processing documents..."):
            try:
                # Load documents from directory
                docs = load_and_split_pdf_directory(
                    doc_directory,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                
                if not docs:
                    st.error(f"❌ No documents found in '{doc_directory}'")
                else:
                    st.success(f"✅ Loaded {len(docs)} document chunks")
                    
                    # Create or recreate index
                    with st.spinner("Creating Pinecone index..."):
                        index_name = "quiz-app-index"
                        vectorstore = create_or_recreate_index(
                            index_name,
                            docs,
                            metric="cosine"
                        )
                        st.session_state.vectorstore = vectorstore
                        st.session_state.index_loaded = True
                        st.success(f"✅ Pinecone index '{index_name}' created and ready!")
                        
            except FileNotFoundError:
                st.error(f"❌ Directory '{doc_directory}' not found. Please check the path.")
            except Exception as e:
                st.error(f"❌ Error loading documents: {str(e)}")

# Main chat interface
st.header("💬 Ask Questions About Your Documents")

if st.session_state.index_loaded and st.session_state.vectorstore:
    st.success("✅ Index loaded. Ready to answer questions!")
    
    # Chat input
    col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
    with col1:
        user_question = st.text_input(
            "Enter your question:",
            key="question_input",
            placeholder="What would you like to know about the documents?"
        )
    with col2:
        ask_button = st.button("🔍 Ask", use_container_width=True, key="ask_btn")
    
    # Process question
    if ask_button and user_question:
        with st.spinner("Searching documents and generating answer..."):
            try:
                answer, retrieved_docs = ask_with_index(
                    user_question,
                    st.session_state.vectorstore,
                    k=k_results
                )
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": answer,
                    "docs": retrieved_docs
                })
                
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")
    
    # Display chat history (latest first)
    if st.session_state.chat_history:
        st.divider()
        st.subheader("💭 Chat History")
        
        for i, interaction in enumerate(reversed(st.session_state.chat_history)):
            with st.container(border=True):
                st.markdown(f"**Q:** {interaction['question']}")
                st.markdown(f"**A:** {interaction['answer']}")
                
                # Show retrieved documents in expander
                with st.expander(f"📄 Retrieved Documents ({len(interaction['docs'])} chunks)"):
                    for j, doc in enumerate(interaction['docs'], 1):
                        st.markdown(f"**Chunk {j}:**")
                        st.text(getattr(doc, "page_content", str(doc))[:500] + "...")
                        st.divider()

else:
    st.info("👈 Use the sidebar to configure and load documents from the specified directory.")
