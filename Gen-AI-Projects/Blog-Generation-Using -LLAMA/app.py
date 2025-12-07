import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import os
from pathlib import Path

## Model configuration
MODEL_NAME = "llama-2-7b-chat.ggmlv3.q8_0.bin"
MODEL_PATH = "models"
FULL_MODEL_PATH = os.path.join(MODEL_PATH, MODEL_NAME)
HUGGINGFACE_MODEL_ID = "TheBloke/Llama-2-7B-Chat-GGML"

def download_model_from_huggingface():
    """Download the model from Hugging Face if not present locally"""
    from huggingface_hub import hf_hub_download
    
    # Create models directory if it doesn't exist
    Path(MODEL_PATH).mkdir(parents=True, exist_ok=True)
    
    st.info(f"📥 Downloading {MODEL_NAME} from Hugging Face...")
    try:
        hf_hub_download(
            repo_id=HUGGINGFACE_MODEL_ID,
            filename=MODEL_NAME,
            local_dir=MODEL_PATH
        )
        st.success(f"✅ Model downloaded successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Failed to download model: {str(e)}")
        return False

def get_model_path():
    """Check if model exists locally, if not download it"""
    if os.path.exists(FULL_MODEL_PATH):
        st.success(f"✅ Model found locally: {FULL_MODEL_PATH}")
        return FULL_MODEL_PATH
    else:
        st.warning(f"⚠️ Model not found at {FULL_MODEL_PATH}. Downloading...")
        if download_model_from_huggingface():
            return FULL_MODEL_PATH
        else:
            return None

## Function to get response from llama2 model

def getLLamaresponse(input_text, no_words, blog_style):
    
    # Get model path (download if needed)
    model_path = get_model_path()
    if not model_path:
        raise Exception("Model could not be loaded or downloaded")

    # LLama2 Model
    llm = CTransformers(model = model_path,
                        model_type = 'llama',
                        config = {'max_new_tokens' : 256,
                                  'temperature' : 0.01
                                 })
    
    # Prompt Template
    template = """ write a blog for {blog_style} on the topic {input_text} in {no_words} words."""

    prompt = PromptTemplate(
        input_variables=["input_text", "no_words", "blog_style"],
        template=template,
    )

    # Generate the response from the model using invoke
    response = llm.invoke(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    print(response)
    return response


st.set_page_config(page_title="Blog Generation using LLaMA2", 
                   page_icon="🤖",
                   layout="centered",
                   initial_sidebar_state="collapsed"
                   )

st.header("Blog Generation using LLaMA2 🤖")

input_text = st.text_input("Enter the topic for the blog:")

## Creating two more columns for additional two fields

col1, col2 = st.columns([5,5])

with col1:
    no_words=st.text_input("Enter number of words for the blog:")

with col2:
    blog_style=st.selectbox("Writing the blog for", ["Researchers", "Data Scientists", "Common People"], index=0)

submit=st.button("Generate Blog")


## Final Response
if submit:
    if not input_text.strip():
        st.error("⚠️ Please enter a blog topic")
    elif not no_words.strip():
        st.error("⚠️ Please enter number of words")
    else:
        with st.spinner("✍️ Generating blog..."):
            try:
                response = getLLamaresponse(input_text, no_words, blog_style)
                st.success("Blog generated successfully!")
                st.markdown("---")
                st.markdown("### 📝 Generated Blog:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error generating blog: {str(e)}")