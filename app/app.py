import streamlit as st
from dotenv import load_dotenv
import json
from workers.worker_classes import ResponseLLM, TaskRecognizer

load_dotenv()

st.title("Speech Analysis App")
response_llm = ResponseLLM()
task_recognizer = TaskRecognizer()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Example how to add python code block to output
# ```python
# for i in range(5):
#     print(i)
# ```

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    chosen_task, date_range = task_recognizer.work(prompt)
    formatted_answer = response_llm.work(st.session_state.messages, chosen_task, date_range)
    with st.chat_message("assistant"):
        response = st.write_stream(formatted_answer)
    st.session_state.messages.append({"role": "assistant", "content": response})