# 🎥 YouTube Video Q&A Chatbot

## Overview

**YouTube Video Q&A Chatbot** is an intelligent web application that allows users to upload any YouTube video and ask natural language questions about its content. The chatbot intelligently searches the video's transcript and provides accurate, context-aware answers using advanced AI technology.

Think of it as having a personal assistant who has watched the entire video and can answer any questions you have about it!

---

## 🌟 Key Features

### For Users
- **Easy URL Input**: Simply paste a YouTube URL to get started
- **Natural Q&A Interface**: Ask questions in plain English about video content
- **Instant Answers**: Get AI-powered responses based on the actual video transcript
- **Chat History**: Keep track of your questions and answers in a conversation view
- **Video Management**: Easily switch between different videos
- **No Prerequisites**: No need to watch the entire video yourself!

### For Technical Teams
- **RAG Architecture**: Uses Retrieval-Augmented Generation for accurate, context-grounded answers
- **Semantic Search**: FAISS vector database for intelligent content retrieval
- **Scalable Design**: Modular code structure for easy maintenance and extension
- **Error Handling**: Robust transcript extraction and processing
- **Modern Stack**: Built with LangChain, Streamlit, and OpenAI GPT-4

---

## 🏗️ How It Works

### The Technology Behind the Magic

1. **Transcript Extraction**: 
   - Automatically fetches the YouTube video transcript using the `youtube-transcript-api`
   - Supports multiple languages with English as default

2. **Text Processing**:
   - Breaks long transcripts into manageable chunks (1000 characters with 200-character overlap)
   - Ensures context continuity between chunks

3. **Embeddings & Vector Storage**:
   - Converts text chunks into semantic embeddings using OpenAI's `text-embedding-3-small` model
   - Stores embeddings in FAISS (Facebook AI Similarity Search) vector database for fast retrieval

4. **Intelligent Retrieval**:
   - When you ask a question, the system finds the 4 most relevant transcript sections
   - Uses similarity search to match your question semantically

5. **Answer Generation**:
   - Combines retrieved context with your question
   - Uses GPT-4o-mini to generate accurate, concise answers
   - Ensures answers are grounded in actual video content

### Architecture Diagram
```
User Query
    ↓
[UI Layer - Streamlit]
    ↓
[Video ID Extraction]
    ↓
[Transcript Fetching]
    ↓
[Text Splitting & Embedding]
    ↓
[FAISS Vector Store]
    ↓
[Similarity Search] ← Retrieves Relevant Chunks
    ↓
[LangChain RAG Chain]
    ↓
[GPT-4o-mini LLM]
    ↓
[Answer Output to User]
```

---

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Windows/Mac/Linux operating system
- Internet connection (for API calls)

### API Keys Needed
- **OpenAI API Key**: Required for GPT-4 and embeddings
  - Sign up at https://platform.openai.com
  - Create API key in account settings
  - Add $5-10 credit for testing

---

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project
```bash
# Navigate to the project directory
cd Youtube-Chatbot
```

### Step 2: Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Run the Application
```bash
streamlit run ui.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### For First-Time Users

1. **Load a Video**
   - Copy any YouTube video URL from your browser
   - Paste it in the "Paste YouTube URL" field in the left sidebar
   - Click "Load Video" button
   - Wait for the system to process (will show a spinner)
   - You'll see a success message when ready

2. **Ask Questions**
   - Type any question about the video in the text area
   - Click the "Send" button (center-aligned)
   - The AI will search the transcript and provide an answer
   - Your question and answer appear in the chat history above

3. **Continue Conversation**
   - Ask as many questions as you want about the same video
   - All questions and answers are stored in the conversation
   - Want a different video? Click "Clear Video" and load a new one

### Example Questions You Can Ask
- "What is the main topic of this video?"
- "Can you summarize the key points?"
- "Who are the speakers and what are their names?"
- "What specific examples were mentioned?"
- "What are the main conclusions?"
- "Explain the technical concepts mentioned"

---

## 📁 Project Structure

```
Youtube-Chatbot/
├── ui.py                    # Main UI application (Streamlit)
├── main.py                  # Backend RAG pipeline logic
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md               # This file
```

### File Descriptions

**ui.py** - User Interface Layer
- Handles all user interactions and visual display
- Manages chat history and conversation flow
- Extracts YouTube video IDs from URLs
- Session state management for user sessions

**main.py** - Backend Processing Layer
- `YouTubeRAGPipeline` class: Core logic for processing videos
- `_fetch_transcript()`: Gets video transcript from YouTube
- `_create_vector_store()`: Creates embeddings and FAISS database
- `_build_chain()`: Sets up the LangChain RAG pipeline
- `answer_question()`: Generates answers to user queries

---

## 🔧 Configuration

### Model Settings (in main.py)

You can customize these parameters:

```python
# Text splitting configuration
chunk_size=1000          # Size of each text chunk
chunk_overlap=200        # Overlap between chunks for context

# Embedding model
model="text-embedding-3-small"  # OpenAI embedding model

# LLM configuration
model="gpt-4o-mini"      # GPT model to use
temperature=0.2          # Lower = more focused, higher = more creative

# Retrieval configuration
search_kwargs={"k": 4}   # Number of relevant chunks to retrieve
```

---

## ⚙️ How to Modify the Project

### Add Different LLM Model
```python
# In main.py, change the model parameter:
llm = ChatOpenAI(model="gpt-4", temperature=0.3)
```

### Adjust Chunk Size for Better Results
```python
# Larger chunks = more context, but may be less focused
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,  # Increase this
    chunk_overlap=400
)
```

### Change Number of Retrieved Documents
```python
# In main.py:
self.retriever = self.vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6}  # Retrieve 6 chunks instead of 4
)
```

---

## 🐛 Troubleshooting

### Issue: "Invalid YouTube URL"
**Solution**: Make sure you're pasting a valid YouTube URL. Supported formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- Just the video ID itself (11 characters)

### Issue: "Transcripts are disabled for this video"
**Solution**: Not all YouTube videos have transcripts. Try a different video, preferably those with English captions enabled.

### Issue: "OpenAI API Key Error"
**Solution**: 
- Verify your API key is correct in the `.env` file
- Make sure you have credits in your OpenAI account
- Check that the API key has not expired

### Issue: "Module not found" errors
**Solution**: 
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Try: `pip install --upgrade -r requirements.txt`

### Issue: Slow responses
**Solution**: 
- OpenAI API calls can take 5-10 seconds
- Larger videos take longer to process initially
- This is normal behavior

---

## 📊 Dependencies Overview

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `langchain-openai` | OpenAI integration for LLM |
| `langchain-community` | FAISS vector store |
| `youtube-transcript-api` | YouTube transcript extraction |
| `faiss-cpu` | Vector similarity search |
| `python-dotenv` | Environment variable management |

---

## 💡 For HR and Non-Technical Stakeholders

### Business Value
- **Time Saving**: Users can get information from videos instantly without watching them completely
- **Accessibility**: Makes video content searchable and accessible
- **Learning Support**: Helps in educational and training contexts
- **Content Analysis**: Can analyze large volume of video content efficiently

### Use Cases
1. **Education**: Students asking questions about lecture videos
2. **Training**: Employees learning from company training videos
3. **Research**: Quickly extracting information from research presentation videos
4. **Content Review**: Analyzing and summarizing long webinars or conferences

### Technology Highlights
- Uses **cutting-edge AI** (GPT-4) for intelligent answers
- **Production-ready code** with proper error handling
- **Scalable architecture** that can handle multiple concurrent users
- **Cost-optimized** using smaller embedding and LLM models

---

## 🔮 Future Enhancements

Potential features for future versions:
- [ ] Multi-language support for questions
- [ ] PDF, website, and document support
- [ ] Answer source citations (timestamps in video)
- [ ] Custom prompt engineering for specific domains
- [ ] Video summarization feature
- [ ] Export chat history as PDF
- [ ] User authentication and history persistence
- [ ] Batch processing for multiple videos
- [ ] Custom knowledge base integration

---

## 📝 Example Workflow

```
1. User opens application → ui.py starts
2. User pastes YouTube URL → extract_video_id() extracts ID
3. System initializes → YouTubeRAGPipeline class created
4. Transcript fetched → _fetch_transcript() runs
5. Vector store built → _create_vector_store() processes chunks
6. RAG chain ready → _build_chain() creates LangChain pipeline
7. User asks question → answer_question() retrieves and generates answer
8. Response displayed → ui.py shows in chat interface
```