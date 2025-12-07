# llm_engine.py
import os
from dotenv import load_dotenv

load_dotenv()  # load .env if present

# --- OpenAI client (new SDK) ---
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Set it in environment or .env")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# --- LangChain / Pinecone pieces ---
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# instantiate embeddings wrapper (used for dimension detection and upsert)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Pinecone initialization helper
from pinecone import Pinecone, ServerlessSpec

def _init_pinecone():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY must be set.")
    pc = Pinecone(api_key=api_key)
    return pc

def _get_pinecone_region():
    """Get Pinecone region from environment, default to us-east-1."""
    return os.getenv("PINECONE_REGION", "us-east-1")

# Delete & recreate index, then upsert docs
def create_or_recreate_index(index_name: str, docs, namespace: str = None, metric: str = "cosine"):
    """
    Deletes the index if exists, creates a fresh index, then upserts `docs`.
    Returns a PineconeVectorStore connected to the new index.
    """
    pc = _init_pinecone()
    
    # Check if index exists and delete it
    existing_indexes = pc.list_indexes().names()
    if index_name in existing_indexes:
        try:
            pc.delete_index(index_name)
            print(f"Deleted existing Pinecone index: {index_name}")
        except Exception as e:
            # if delete fails, still attempt to continue (raise if you prefer)
            print(f"Warning: failed to delete index {index_name}: {e}")

    # Determine dimension for embeddings
    try:
        test_emb = embeddings.embed_query("test")
        dimension = len(test_emb)
    except Exception:
        # fallback to common dimension for many OpenAI embeddings
        dimension = 1536
        print("Could not compute embedding dimension dynamically; falling back to 1536.")

    # Create the index with ServerlessSpec
    try:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud='aws',
                region=_get_pinecone_region()
            )
        )
        print(f"Created Pinecone index: {index_name} (dim={dimension}, metric={metric})")
    except Exception as e:
        # If creation fails, raise — better to stop than to continue with unknown index
        raise RuntimeError(f"Failed to create Pinecone index '{index_name}': {e}")

    # Upsert documents using LangChain PineconeVectorStore helper
    vectorstore = PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        index_name=index_name,
        namespace=namespace
    )

    return vectorstore

# PDF loader + splitter
def load_and_split_pdf(pdf_path, chunk_size=1000, chunk_overlap=200):
    """
    Loads a single PDF file from pdf_path and returns a list of langchain Document chunks.
    """
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(pages)
    return chunks

def load_and_split_pdf_directory(directory, chunk_size=1000, chunk_overlap=200):
    """
    Loads all PDF files from a directory and returns a list of langchain Document chunks.
    """
    loader = PyPDFDirectoryLoader(directory)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(pages)
    return chunks

# Simple QA using OpenAI completions v1 (client.completions.create)
def ask_with_index(query, index, k=4, model="gpt-3.5-turbo-instruct", max_tokens=250):
    """
    Query the index (PineconeVectorStore), build a single prompt (stuff-style),
    call OpenAI completions API via new SDK client.completions.create, return string.
    """
    docs = index.similarity_search(query, k=k)
    if not docs:
        return "No documents found for the query.", []

    context = "\n\n".join(getattr(d, "page_content", str(d)) for d in docs)
    prompt = (
        "Answer the following question based ONLY on the provided context. "
        "If the answer is not contained, respond: \"I don't know\".\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )

    resp = openai_client.completions.create(
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.0
    )

    # resp.choices[0].text is expected shape
    try:
        answer = resp.choices[0].text.strip()
    except Exception:
        # fallback to str
        answer = str(resp)

    return answer, docs
