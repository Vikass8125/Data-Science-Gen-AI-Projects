import streamlit as st
import re
from main import YouTubeRAGPipeline

# Set up page configuration
st.set_page_config(page_title="YouTube Q&A Chatbot", layout="wide")
st.title("🎥 YouTube Video Q&A Chatbot")

# Initialize session state for pipeline and messages
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_video_id" not in st.session_state:
    st.session_state.current_video_id = None


def extract_video_id(youtube_url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - youtube.com/watch?v=VIDEO_ID
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/?)?.*[?&]v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    # If it's already just the video ID (11 characters)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', youtube_url.strip()):
        return youtube_url.strip()
    
    return None


def initialize_pipeline(video_id: str):
    """Initialize the RAG pipeline with a YouTube video."""
    try:
        with st.spinner(f"Processing YouTube video {video_id}... This may take a moment."):
            st.session_state.rag_pipeline = YouTubeRAGPipeline(video_id)
            st.session_state.current_video_id = video_id
            st.session_state.messages = []  # Clear chat history for new video
        st.success("✅ Video processed successfully! You can now ask questions.")
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        st.session_state.rag_pipeline = None


# Sidebar for video input
with st.sidebar:
    st.header("📝 Video Input")
    st.write("Enter a YouTube video URL to start asking questions about its content.")
    
    youtube_url = st.text_input(
        label="Paste YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste a full YouTube URL or just the video ID"
    )
    
    if st.button("🔄 Load Video", use_container_width=True, type="primary"):
        if not youtube_url:
            st.warning("⚠️ Please paste a YouTube URL")
        else:
            video_id = extract_video_id(youtube_url)
            if video_id:
                initialize_pipeline(video_id)
            else:
                st.error("❌ Invalid YouTube URL. Please check and try again.")
    
    if st.session_state.current_video_id:
        st.info(f"📌 Current Video ID: `{st.session_state.current_video_id}`")
        if st.button("🗑️ Clear Video", use_container_width=True):
            st.session_state.rag_pipeline = None
            st.session_state.messages = []
            st.session_state.current_video_id = None
            st.rerun()


# Main chat area
st.header("💬 Ask Questions About the Video")

if st.session_state.rag_pipeline is None:
    st.info("👈 Please load a YouTube video from the sidebar to get started!")
else:
    # Display chat history
    st.subheader("Chat History")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    st.subheader("Your Question")
    user_question = st.text_area(
        label="Ask a question about the video content:",
        placeholder="What is the main topic of the video?",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        submit_button = st.button("📤 Send", use_container_width=True, type="primary")
    
    if submit_button:
        if not user_question.strip():
            st.warning("⚠️ Please enter a question")
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_question})
            
            # Get response from RAG pipeline
            with st.spinner("🔍 Searching for relevant content..."):
                try:
                    response = st.session_state.rag_pipeline.answer_question(user_question)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error getting response: {str(e)}")
    

