import streamlit as st
from openai import OpenAI

st.title("My Lab3")
OpenAI_model= st.sidebar.selectbox("Which Model should I use?",("mini","regular"))

if OpenAI_model== "mini":
    model_to_use ="gpt-4o-mini"
else:
    model_to_use= "gpt-4o-mini"

if 'client' not in st.session_state:
    api_key=st.secrets["open_ai_key"]
    st.session_state.client=OpenAI(api_key="open_ai_key")

if 'messages' not in st.session_state:
    st.session_state["messages"]=\
        [{"roles":"assistant","content":"How can I help you?"}]

for msg in st.session_state.messages:
    chat_msg=st.chat_message(msg["roles"])

if prompt:=st.chat_input("Heyy"):
    st.session_state.messages.append({"roles":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    client=st.session_state.client
    stream = client.chat.completions.create(
        model=model_to_use,
        messages=st.session_state.messages,
        stream=True
    )
    
    with st.chat_message("assistant"):
        response=st.write_stream(stream)
    st.session_state.messages.append({"role":"assistant","content":response})
