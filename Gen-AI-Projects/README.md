# 🤖 Gen-AI Projects Overview

Welcome to the **Gen-AI Projects** collection! This document provides a quick overview of all projects in this repository. Click on any project title to view its detailed README.

---

## 📋 Project Directory

| # | Project | Description |
|---|---------|-------------|
| 1 | [🧠 Local Blog Generator using LLaMA-2](#blog-generation-using-llama) | Create blog drafts instantly using a fully offline AI model — simple, private, and requires no API keys. |
| 2 | [💬 Gemini Conversational Chatbot](#conversational-qanda-chatbot-using-gemini-pro) | A conversational AI chatbot built with Google Gemini and Streamlit featuring real-time streaming responses and session-based memory. |
| 3 | [📄 PDF Summarizer](#pdf-summarization-tool) | Upload PDFs and receive concise AI-generated summaries using RAG workflow with LangChain, FAISS, and OpenAI. |
| 4 | [📚 Quiz App - Chat with Documents](#quiz-app-pinecone) | Chat with your PDF documents using a RAG pipeline built on Pinecone, LangChain, and OpenAI. |
| 5 | [🎥 YouTube Video Q&A Chatbot](#youtube-video-qa-chatbot) | Ask intelligent questions about any YouTube video. The AI analyzes transcripts and provides context-aware answers using RAG with LangChain and GPT-4. |

---

## 🚀 Projects

### 🧠 Local Blog Generator using LLaMA-2

**Directory:** `Blog-Generation-Using-LLAMA/`

**[📖 View Full README](./Blog-Generation-Using%20-LLAMA/README.md)**

#### Overview
A beginner-friendly local blog generator that creates blog drafts instantly without requiring internet or API keys. This project solves common problems with online AI tools by running everything offline on your own device.

#### Key Features
- 🔒 **Full Privacy:** Nothing is sent to the internet
- ⚡ **Fast Generation:** Usually 10-30 seconds on a normal laptop
- 📝 **Customizable:** Choose blog topic, word count, and writing style
- 🤖 **Offline AI:** Uses LLaMA-2 GGML model with CTransformers
- 📦 **Auto-Download:** Automatically downloads model from HuggingFace if needed

#### Problem It Solves
- Online AI tools require internet connectivity
- Many require paid API keys
- Sensitive content may be sent to the cloud

#### How It Works
1. User enters blog topic, word count, and writing style
2. App checks if model exists in `models/` folder
3. Model auto-downloads from HuggingFace if needed
4. CTransformers loads the model on your CPU
5. AI generates complete blog locally
6. Blog appears in Streamlit interface

---

### 💬 Gemini Conversational Chatbot

**Directory:** `Conversational-QandA-Chatbot-Using-Gemini-Pro/`

**[📖 View Full README](./Conversational-QandA-Chatbot-Using-Gemini-Pro/README.md)**

#### Overview
A modern conversational AI chatbot built with Google Gemini (gemini-2.5-flash) and Streamlit. It demonstrates professional LLM integration with real-time streaming responses and chat memory management.

#### Key Features
- 🌊 **Real-time Streaming:** Responses appear chunk-by-chunk for smooth interaction
- 💾 **Session Memory:** Maintains running chat history like a real chatbot
- 🎯 **Google Gemini Integration:** Uses cutting-edge gemini-2.5-flash model
- 🎨 **Clean UI:** Lightweight, production-friendly Streamlit interface
- 📱 **Interactive:** Natural language question answering

#### Perfect For
- Demonstrating LLM integration skills
- Rapid prototyping at work
- Building internal chatbots
- Showcasing GenAI expertise in your portfolio

#### Architecture
```
User Question → Streamlit App → GOOGLE_API_KEY (.env) → 
Google Gemini Client → gemini-2.5-flash Model → 
Streaming Response → Session Memory → Updated UI
```

---

### 📄 PDF Summarizer using LangChain & OpenAI

**Directory:** `PDF-Summarization-Tool/`

**[📖 View Full README](./PDF-Summarization-Tool/README.md)**

#### Overview
A PDF Summarization application that uses Retrieval-Augmented Generation (RAG) to produce accurate, grounded summaries. Built with Streamlit, LangChain, FAISS, and OpenAI GPT models.

#### Key Features
- 📤 **Easy Upload:** Upload any PDF through Streamlit UI
- 📚 **Smart Extraction:** PyPDF extracts text from all pages
- 🔗 **LangChain Pipeline:** Professional text splitting and embeddings
- 🗂️ **FAISS Vector DB:** Semantic search over document content
- 🎯 **Grounded Summaries:** No hallucinations—summaries based on actual content
- 🚀 **GPT-3.5-Turbo:** Uses advanced language model for quality summaries

#### RAG Workflow
```
PDF Upload → Text Extraction → Text Chunking → 
Embeddings Generation (HuggingFace) → FAISS Vector Store → 
Retrieval (Top-5 chunks) → LLM Summarization → 
Final Summary Output
```

#### Tech Stack
- **Streamlit** - User interface
- **PyPDF** - PDF text extraction
- **LangChain** - Text processing and chaining
- **FAISS** - Vector database
- **HuggingFace Embeddings** - `sentence-transformers/all-MiniLM-L6-v2`
- **OpenAI** - `gpt-3.5-turbo-16k` for summarization

---

### 📚 Quiz App - Chat with Your Documents (RAG + Pinecone)

**Directory:** `Quiz-App-Pinecone/`

**[📖 View Full README](./Quiz-App-Pinecone/README.md)**

#### Overview
An intelligent document Q&A system that lets you chat with PDFs. Users can load a folder of documents, index them with Pinecone, and ask questions that are answered using only the document content—perfect for building knowledge bases and internal documentation systems.

#### Key Features
- 📁 **Folder Loading:** Load any directory containing PDFs
- 🔄 **Auto Chunking:** Automatically splits PDF pages into overlapping chunks
- 🗂️ **Pinecone Index:** Creates fresh index for semantic search
- 🔍 **Semantic Retrieval:** Finds most relevant chunks using vector similarity
- 💬 **Chat Interface:** Beautiful conversation history with supporting chunks
- ⚙️ **Customizable:** Adjust chunk size, overlap, and retrieval count

#### RAG Pipeline Flow
```
PDF Folder Selection → PDF Loading (PyPDFDirectoryLoader) → 
Text Chunking (RecursiveCharacterTextSplitter) → 
Embeddings Generation (OpenAI) → 
Pinecone Index Creation → 
Document Vector Upsert → 
User Question → 
Semantic Retrieval (Top-K) → 
Prompt Construction → 
OpenAI Response Generation → 
Answer with Context
```

#### Tech Stack
- **Pinecone** - Vector database for semantic search
- **LangChain** - Document processing and retrieval
- **OpenAI** - Embeddings and LLM
- **Streamlit** - User interface
- **PyPDF** - PDF document loading

---

### 🎥 YouTube Video Q&A Chatbot

**Directory:** `Youtube-Chatbot/`

**[📖 View Full README](./Youtube-Chatbot/README.md)**

#### Overview
An intelligent Q&A system that allows users to ask natural language questions about any YouTube video content. The chatbot automatically extracts video transcripts and uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware answers. No need to watch entire videos anymore!

#### Key Features
- 🎬 **YouTube URL Support:** Paste any YouTube URL and start asking questions
- 📝 **Automatic Transcript Extraction:** Fetches video transcripts automatically
- 🤖 **AI-Powered Answers:** Uses GPT-4o-mini to generate intelligent responses
- 🔍 **Semantic Search:** FAISS vector database for fast, accurate retrieval
- 💬 **Chat Interface:** Beautiful conversation history with all Q&A
- 🎯 **Context-Grounded:** Answers based on actual video content, never hallucinations

#### Perfect For
- Students wanting answers from lecture videos
- Professionals analyzing webinars or presentations
- Researchers extracting information from videos
- Content creators reviewing videos
- Anyone who wants to learn without watching the full video

#### RAG Architecture
```
YouTube URL → Video ID Extraction → Transcript Fetching → 
Text Chunking → Embeddings Generation → FAISS Vector Store → 
Semantic Search → GPT-4o-mini Answer Generation
```

#### Tech Stack
- **Streamlit** - User interface and session management
- **LangChain** - RAG pipeline orchestration
- **FAISS** - Vector similarity search database
- **OpenAI** - GPT-4o-mini LLM & embeddings
- **youtube-transcript-api** - YouTube transcript extraction
- **Python-dotenv** - Environment variables

---

## 🛠️ Getting Started

Each project has its own directory with:
- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation

To get started with any project:

1. Navigate to the project directory
2. Read the project's README file (click the link above)
3. Install dependencies: `pip install -r requirements.txt`
4. Set up required API keys (if needed)
5. Run the app: `streamlit run app.py`

---

## 📝 Notes

- All projects use **Streamlit** for the user interface
- Most projects integrate with **OpenAI** or **Google APIs**
- Each project demonstrates different GenAI patterns (generation, conversation, retrieval, RAG)
- See individual README files for detailed setup instructions

---

**Last Updated:** December 2025

For questions or improvements, refer to the individual project README files.
