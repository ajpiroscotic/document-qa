import streamlit as st
import requests
from bs4 import BeautifulSoup

def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

def summarize_text(text, summary_type, language, llm_model, use_advanced_model):
    # Placeholder function for text summarization
    # You should replace this with your actual summarization logic
    summary = ""
    if summary_type == "Short":
        summary = text[:100] + "..."
    elif summary_type == "Medium":
        summary = text[:200] + "..."
    else:  # Long
        summary = text[:300] + "..."
    
    # Placeholder for translation and LLM processing
    # In a real application, you would use a translation API and the selected LLM here
    summary = f"Summary using {llm_model} ({'advanced' if use_advanced_model else 'standard'} model):\n\n"
    if language == "English":
        summary += f"English summary: {summary}"
    elif language == "French":
        summary += f"Résumé en français: {summary}"
    elif language == "Spanish":
        summary += f"Resumen en español: {summary}"
    else:
        summary += f"Summary in {language}: {summary}"
    
    return summary

st.set_page_config(page_title="URL Content Summarizer")

st.title("URL Content Summarizer")

# URL input at the top of the screen
url = st.text_input("Enter a URL:")

# Sidebar options
with st.sidebar:
    st.header("Settings")
    summary_type = st.selectbox(
        "Select summary type:",
        ("Short", "Medium", "Long")
    )
    
    output_language = st.selectbox(
        "Select output language:",
        ("English", "French", "Spanish")
    )
    
    llm_model = st.selectbox(
        "Select LLM model:",
        ("OpenAI", "Claude", "Gemini")
    )
    
    use_advanced_model = st.checkbox("Use advanced model", value=False)

if url:
    content = read_url_content(url)
    if content:
        summary = summarize_text(content, summary_type, output_language, llm_model, use_advanced_model)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Unable to retrieve content from the URL.")
else:
    st.info("Please enter a URL to summarize its content.")