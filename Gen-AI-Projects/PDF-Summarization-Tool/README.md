# 📄 PDF Summarizer using LangChain, FAISS, HuggingFace Embeddings, and OpenAI

# 🚀 Overview

This project is a **PDF Summarization Application** built with:

* **Streamlit** for the user interface,
* **PyPDF** for PDF text extraction,
* **LangChain** components for text splitting, embeddings, retrieval, and LLM chaining,
* **FAISS** for vector-based semantic search,
* **OpenAI GPT (gpt-3.5-turbo-16k)** for generating concise summaries.

The app allows a user to upload any PDF file and receive a clear, concise summary generated using a Retrieval-Augmented Generation (RAG) workflow.

---

# ✨ Features

* Upload any PDF file through the Streamlit UI.
* Extracts text from all pages using `pypdf`.
* Splits text into chunks for better embedding + retrieval.
* Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
* Stores chunks in a **FAISS vector database**.
* Runs a **retrieval + LLM chain** to produce an accurate summary.
* No hallucinations — summary is grounded in retrieved content.

---

# 🧠 How It Works

Below is the flow of the entire summarization pipeline:

```
User Uploads PDF
        ↓
Extract Text Using PyPDF
        ↓
Split Text Into Chunks (LangChain TextSplitter)
        ↓
Generate Embeddings (HuggingFaceEmbeddings)
        ↓
Store Vectors in FAISS Vector Database
        ↓
Retriever Fetches Most Relevant Chunks (k=5)
        ↓
LLM (GPT-3.5-Turbo-16k) Summarizes Retrieved Content
        ↓
Return Final Summary to Streamlit UI
```

A clean, structured RAG pipeline designed specifically for summarization.

---

# 🏗️ Architecture Diagram (Text Version)

```
                  ┌───────────────────┐
                  │  Streamlit UI     │
                  │  (Upload PDF)     │
                  └─────────┬─────────┘
                            ↓
                   Extract Text (pypdf)
                            ↓
         ┌──────────────────────────────┐
         │  Text Splitter (1000 tokens) │
         └────────────────────┬─────────┘
                              ↓
                Generate Embeddings
        (sentence-transformers / MiniLM-L6-v2)
                              ↓
                        FAISS Index
                 (Stores dense vectors)
                              ↓
                  Retriever (Top-k = 5)
                              ↓
                  OpenAI GPT LLM Chain
             (RAG-based Summarization)
                              ↓
                  Streamlit Summary Output
```

---

# 🔍 Technical Breakdown

A deeper explanation of each major component.

## 1. PDF Text Extraction

Library: **pypdf**

* Reads PDF binary stream.
* Extracts text page by page.
* Concatenates pages into a single raw text string.

Snippet from the project:  fileciteturn2file2

```python
reader = PdfReader(io.BytesIO(pdf_bytes))
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() or ""
```

---

## 2. Text Splitting (Chunking)

Library: **langchain_text_splitters**

* Splits large text into overlapping segments.
* Chunk size: 1000 characters.
* Overlap: 200 characters.

Why?

* LLMs and retrieval work better with smaller, coherent chunks.

Snippet:

```python
splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
chunks = splitter.split_text(text)
```

---

## 3. Embedding Generation

Library: **HuggingFaceEmbeddings** using `sentence-transformers/all-MiniLM-L6-v2`.

* Converts text chunks into 384-dimensional dense vectors.
* Captures semantic meaning rather than keywords.

Why MiniLM?

* Lightweight
* Fast
* High accuracy for semantic similarity

Snippet:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

---

## 4. Vector Store — FAISS (Local Vector Database)

Library: **faiss-cpu**

* Stores all chunk embeddings.
* Supports efficient similarity search.
* Ideal for local RAG applications.

Snippet:

```python
vector_store = FAISS.from_texts(chunks, embeddings)
```

Retriever used:

```python
retriever = kb.as_retriever(search_kwargs={"k": 5})
```

---

## 5. LLM Summarization (RAG)

Library: **langchain_openai**
Model used: **gpt-3.5-turbo-16k**

* Handles long documents.
* Produces accurate and concise summaries.

Snippet:

```python
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.6)
```

---

## 6. RetrievalQA Chain

Library: **langchain_classic.chains.retrieval_qa.base**

* Combines retriever + LLM into one chain.
* Ensures LLM sees only top-k relevant chunks.
* Prevents hallucinations.

Snippet:

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)
result = qa_chain.run(query)
```

---

# 🎛️ Streamlit Interface

Main UI file: **test.py**  fileciteturn2file1

* Upload widget for PDF files.
* Button triggers summarization.
* Displays the final summary cleanly.

Snippet:

```python
pdf_file = st.file_uploader("Upload your PDF file", type=["pdf"])
submit = st.button("Summarize")
...
st.write(summary)
```

---

# ▶️ How to Run the Project

```
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Run the app:

```
streamlit run test.py
```

---

# 📌 Requirements (From requirements.txt)

Technologies used:  fileciteturn2file0

```
streamlit
pypdf
openai
sentence-transformers
faiss-cpu
langchain
langchain-huggingface
langchain-text-splitters
langchain-community
langchain-openai
python-dotenv
```


