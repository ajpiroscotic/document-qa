import streamlit as st
import requests
from bs4 import BeautifulSoup # type: ignore
from openai import OpenAI
import google.generativeai as genai # type: ignore
from anthropic import Anthropic # type: ignore

def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

def validate_api_key(api_key, llm_model):
    if not api_key:
        st.error(f"Please enter your {llm_model} API key.")
        return False
    
    try:
        if llm_model == "OpenAI":
            client = OpenAI(api_key=api_key)
            client.models.list()
        elif llm_model == "Claude":
            client = Anthropic(api_key=api_key)
            client.completions.create(
                model="claude-2.1",
                max_tokens_to_sample=10
            )
        elif llm_model == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
        
        st.success(f"{llm_model} API key is valid!")
        return True
    except Exception as e:
        st.error(f"Invalid {llm_model} API key: {e}")
        return False

def summarize_text(text, summary_type, language, llm_model, api_key):
    prompt = f"Summarize the following text in a {summary_type.lower()} format and translate to {language}:\n\n{text}"
    
    if llm_model == "OpenAI":
        client = OpenAI(api_key="open_ai_key")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
    elif llm_model == "Claude":
        client = Anthropic(api_key="claude_key")
        response = client.completions.create(
            model="claude-2.1",
            max_tokens_to_sample=300,
            prompt=f"Human: {prompt}\n\nAssistant:"
        )
        summary = response.completion
    elif llm_model == "Gemini":
        genai.configure(api_key="gemini_key")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        summary = response.text
    
    return summary

st.set_page_config(page_title="URL Content Summarizer")
st.title("URL Content Summarizer")

url = st.text_input("Enter a URL:")

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
    
    api_key = st.text_input(f"{llm_model} API Key", type="password")
    
    if st.button("Validate API Key"):
        st.session_state.api_key_valid = validate_api_key(api_key, llm_model)

if url and st.session_state.get('api_key_valid', False):
    content = read_url_content(url)
    if content:
        summary = summarize_text(content, summary_type, output_language, llm_model, api_key)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Unable to retrieve content from the URL.")
elif url:
    st.warning("Please enter and validate your API key before summarizing content.")
else:
    st.info("Please enter a URL to summarize its content.")