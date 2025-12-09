# 📚 Quiz App — Chat with Your Documents (RAG + Pinecone + OpenAI)

# 🚀 Overview

This project allows users to **chat with the content of PDF documents** stored inside a specified folder. It uses a Retrieval-Augmented Generation (RAG) pipeline built on:

* **Pinecone** (vector database),
* **LangChain** (document loaders, text splitting, embeddings, retrieval),
* **OpenAI GPT models**, and
* A **Streamlit** interface.

Users can upload or reference a folder of PDF documents, index them, and ask any question related to the contents. The system retrieves the most relevant chunks from Pinecone and generates an answer using only the provided context.

---

# ✨ Features

* Load any directory containing PDFs.
* Automatically split PDF pages into overlapping chunks.
* Create or recreate a fresh Pinecone index when loading documents.
* Query the index using semantic similarity.
* Display the answer along with retrieved supporting chunks.
* Adjustable chunk size, overlap, and top-k retrieval count.
* Clean chat interface with conversation history.

---

# 🧠 How the System Works

Below is the end-to-end flow of the RAG pipeline used in the Quiz App:

```
User Selects PDF Folder
        ↓
Load PDFs (PyPDFDirectoryLoader)
        ↓
Split into Chunks (RecursiveCharacterTextSplitter)
        ↓
Generate Embeddings (OpenAIEmbeddings)
        ↓
Create/Recreate Pinecone Index
        ↓
Upsert Document Vectors
        ↓
User Asks a Question
        ↓
Retrieve Top-K Relevant Chunks
        ↓
Construct Prompt with Retrieved Context
        ↓
Generate Answer using OpenAI LLM
        ↓
Display Chat History + Retrieved Chunks
```

A standard, production-ready Retrieval-Augmented Generation pipeline.

---

# 🏗️ Architecture Diagram (Text Version)

```
 ┌─────────────────────────────┐
 │        Streamlit UI         │
 │ - Configure directory       │
 │ - Set chunk size, overlap   │
 │ - Ask questions             │
 └───────────────┬─────────────┘
                 ↓
      Load PDFs from Directory
     (LangChain PDF Loader)
                 ↓
 ┌───────────────────────────────────────┐
 │ Split Documents using RecursiveCharacterSplitter │
 └───────────────────────────────────────┘
                 ↓
     Embed Chunks using OpenAIEmbeddings
                 ↓
 ┌───────────────────────────────────────┐
 │ Create or Recreate Pinecone Index     │
 │ Upsert Embedded Chunks                │
 └───────────────────────────────────────┘
                 ↓
     User Question Sent to Vectorstore
                 ↓
 Retrieve Top-K Similar Document Chunks
                 ↓
 Construct Prompt → Send to OpenAI LLM
                 ↓
      Generate Final Answer
                 ↓
 Display Answer + Retrieved Chunks in UI
```

---

# 🔍 Technical Breakdown

This section explains each major technical component of the project.

---

## 1. Document Loading & Processing

Code Reference: `load_and_split_pdf_directory`

* Uses **PyPDFDirectoryLoader** to load all PDFs from a directory.
* Uses **RecursiveCharacterTextSplitter** to create overlapping chunks.
* Chunk size and overlap are adjustable via UI sliders.

Why this is important:

* Chunking improves retrieval granularity.
* Overlap helps preserve context across chunk boundaries.

Snippet:

```python
loader = PyPDFDirectoryLoader(directory)
pages = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
chunks = splitter.split_documents(pages)
```

---

## 2. Embedding Generation

Library: **OpenAIEmbeddings**
Reference: embeddings instance in `llm_engine.py`

* Each chunk is converted into a vector representation.
* Embedding dimension is detected dynamically.

Snippet:

```python
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
```

---

## 3. Pinecone Vector Index

Function: `create_or_recreate_index`

This function does the heavy lifting:

* Initializes Pinecone client.
* Deletes existing index (if any).
* Computes embedding dimension and creates a new index.
* Upserts all document chunks using `PineconeVectorStore`.

Snippet:

```python
vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    index_name=index_name
)
```

Benefits:

* Clean reindexing every time.
* Allows switching document sets easily.
* Ensures vectorstore is always in sync.

---

## 4. Retrieval Step

When the user asks a question:

* Pinecone similarity search (`k` adjustable in UI) retrieves top‑k chunks.

Snippet:

```python
docs = index.similarity_search(query, k=k)
```

---

## 5. Prompt Construction & Answer Generation

LLM used: **OpenAI GPT-3.5 Turbo Instruct**
Method: `openai_client.completions.create`  

A single prompt is constructed using the retrieved chunks:

```python
prompt = (
    "Answer the following question based ONLY on the provided context. "
    "If the answer is not contained, respond: \"I don't know\".\n\n"
    f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
)
```

Then the model generates a grounded answer.

---

## 6. Streamlit UI Logic

Reference: `app.py`  

* Allows configuration of chunk size, overlap, directory path.
* Shows status messages while loading docs and creating index.
* Displays answer and retrieved chunks with expanders.
* Maintains conversation history.

Snippet:

```python
if ask_button and user_question:
    answer, retrieved_docs = ask_with_index(user_question, st.session_state.vectorstore, k=k_results)
```

---

# ▶️ How to Run the Project

Install dependencies:

```
pip install -r requirements.txt
```

Environment variables required:

```
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_REGION=us-east-1  # or your region
```

Run the app:

```
streamlit run app.py
```

---

# 📦 Requirements (from requirements.txt)

Technologies used:  fileciteturn3file2

```
unstructured
tiktoken
pinecone-client
pypdf
openai
langchain
langchain-openai
langchain-pinecone
langchain-community
pandas
numpy
python-dotenv
streamlit
langchain-text-splitters
```

