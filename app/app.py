import streamlit as st
from dotenv import load_dotenv
import json
from worker_utils.workers import stream_ollama_response

load_dotenv()

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
        base_prompt = "You will be given history of our conversation. Using it as context (if there is any) answer to my newest message. If there is no context yet don't mention it. "
        response = st.write_stream(stream_ollama_response(base_prompt + json.dumps(st.session_state.messages)))
    st.session_state.messages.append({"role": "assistant", "content": response})