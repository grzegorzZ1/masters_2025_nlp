import streamlit as st
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

def stream_ollama_response(prompt):
    """
    Stream responses from Ollama API with real-time output
    """
    
    payload = {
        "model": os.getenv("MODEL_NAME"),
        "prompt": prompt,
        "stream": True
    }
    
    try:
        response = requests.post(
            "http://ollama:11434/api/generate", 
            json=payload, 
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        yield chunk['response']

                    if chunk.get('done', False):
                        break
                        
                except json.JSONDecodeError:
                    continue
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

st.title("Speech Analysis App")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        response = st.write_stream(stream_ollama_response(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})