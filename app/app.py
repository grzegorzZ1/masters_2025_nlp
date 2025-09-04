import streamlit as st
from dotenv import load_dotenv
import json
from workers.worker_classes import *

load_dotenv()

st.title("Speech Analysis App")
final_response_llm = FinalResponseLLM()
invalid_fields_response_llm = InvalidResponseLLM()
task_recognizer = TaskRecognizer()
field_validator = FieldValidator()
field_inputer = FieldInputer()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chosen_task" not in st.session_state:
    st.session_state.chosen_task = None

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
    if not st.session_state.chosen_task:
        st.session_state.chosen_task = task_recognizer.work(prompt)
    st.session_state.chosen_task = field_inputer.work(st.session_state.chosen_task, prompt)
    invalid_fields = field_validator.work(st.session_state.chosen_task)
    if len(invalid_fields) == 0:
        formatted_answer = final_response_llm.work(st.session_state.chosen_task)
        st.session_state.chosen_task = None
    else:
        formatted_answer = invalid_fields_response_llm.work(st.session_state.chosen_task, invalid_fields)
        st.session_state.chosen_task = field_inputer.work(st.session_state.chosen_task, prompt)
    with st.chat_message("assistant"):
        response = st.write_stream(formatted_answer)
    st.session_state.messages.append({"role": "assistant", "content": response})
