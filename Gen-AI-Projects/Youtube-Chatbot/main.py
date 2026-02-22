import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class YouTubeRAGPipeline:
    """
    A RAG (Retrieval Augmented Generation) pipeline for answering questions about YouTube videos.
    """
    
    def __init__(self, video_id: str):
        """
        Initialize the RAG pipeline with a YouTube video.
        
        Args:
            video_id (str): The YouTube video ID
            
        Raises:
            TranscriptsDisabled: If transcripts are disabled for the video
            Exception: If transcript cannot be fetched
        """
        self.video_id = video_id
        self.transcript = None
        self.vector_store = None
        self.retriever = None
        self.chain = None
        
        # Initialize the pipeline
        self._fetch_transcript()
        self._create_vector_store()
        self._build_chain()
    
    def _fetch_transcript(self):
        """Fetch the YouTube video transcript."""
        try:
            transcript_list = YouTubeTranscriptApi().fetch(self.video_id, languages=['en'])
            self.transcript = " ".join(chunk.text for chunk in transcript_list)
            
            if not self.transcript:
                raise Exception("Transcript is empty")
        
        except TranscriptsDisabled:
            raise Exception(f"Transcripts are disabled for video {self.video_id}")
        except Exception as e:
            raise Exception(f"Failed to fetch transcript: {str(e)}")
    
    def _create_vector_store(self):
        """Create a FAISS vector store from the transcript."""
        try:
            # Split the transcript into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = splitter.create_documents([self.transcript])
            
            # Create embeddings and vector store
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.vector_store = FAISS.from_documents(chunks, embeddings)
            
            # Create retriever
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
        except Exception as e:
            raise Exception(f"Failed to create vector store: {str(e)}")
    
    def _build_chain(self):
        """Build the LangChain RAG chain."""
        try:
            # Initialize LLM
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
            
            # Create prompt template
            prompt = PromptTemplate(
                template="""
You are a helpful assistant answering questions about a YouTube video transcript.
Answer only based on the provided transcript context.
If the context doesn't contain enough information to answer the question, say "I don't have enough information from the video to answer that question."

Transcript Context:
{context}

Question: {question}

Answer:""",
                input_variables=["context", "question"]
            )
            
            # Create document formatter
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            # Build the chain
            parallel_chain = RunnableParallel({
                'context': self.retriever | RunnableLambda(format_docs),
                'question': RunnablePassthrough()
            })
            
            # Final chain: retrieve + format + prompt + llm + parse output
            self.chain = (
                parallel_chain
                | prompt
                | llm
                | StrOutputParser()
            )
        except Exception as e:
            raise Exception(f"Failed to build chain: {str(e)}")
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question about the YouTube video.
        
        Args:
            question (str): The question to answer
            
        Returns:
            str: The answer based on the video transcript
        """
        try:
            if not self.chain:
                raise Exception("Chain not initialized")
            
            response = self.chain.invoke(question)
            return response
        except Exception as e:
            raise Exception(f"Failed to get answer: {str(e)}")
    
    def get_video_id(self) -> str:
        """Get the current video ID."""
        return self.video_id
    
    def get_transcript_preview(self, num_chars: int = 500) -> str:
        """
        Get a preview of the transcript.
        
        Args:
            num_chars (int): Number of characters to return
            
        Returns:
            str: Preview of the transcript
        """
        if self.transcript:
            return self.transcript[:num_chars]
        return "No transcript available"


# Example usage (for testing)
if __name__ == "__main__":
    # Example video ID
    video_id = "kFGCyVTAn50"
    
    try:
        print(f"Initializing RAG pipeline for video: {video_id}")
        pipeline = YouTubeRAGPipeline(video_id)
        
        print(f"\n✅ Successfully loaded video transcript!")
        print(f"\nTranscript preview:\n{pipeline.get_transcript_preview(300)}\n")
        
        # Example questions
        questions = [
            "What is the main topic of this video?",
            "Can you summarize the key points?",
        ]
        
        for question in questions:
            print(f"\nQuestion: {question}")
            answer = pipeline.answer_question(question)
            print(f"Answer: {answer}\n")
            print("-" * 80)
    
    except Exception as e:
        print(f"Error: {e}")
