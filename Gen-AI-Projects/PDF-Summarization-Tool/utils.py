# utils.py
import io
from pypdf import PdfReader

from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

def process_text(text: str) -> FAISS:
    """
    Split the given text into chunks and build a FAISS vectorstore using embeddings.
    """
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def summarize_pdf(uploaded_file) -> str:
    """
    Read the uploaded PDF (Streamlit UploadedFile), extract all text,
    build vectorstore, and run a retrieval + LLM chain to return a concise summary.
    """
    pdf_bytes = uploaded_file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))

    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""

    # Build knowledge base
    kb = process_text(full_text)

    # Set the summarization query
    query = "Provide a concise summary of the document."

    # Create retriever
    retriever = kb.as_retriever(search_kwargs={"k": 5})

    # Initialize LLM (OpenAI chat)
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.6)

    # Build and run the retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    result = qa_chain.run(query)
    return result
