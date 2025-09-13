import streamlit as st
from dotenv import load_dotenv
import json
from workers.worker_classes.chat_workers import *
import pickle

load_dotenv()

st.set_page_config("Task Recognizer Chat")
st.title("Task Recognizer Chat")
final_response_llm = FinalResponseLLM()
invalid_fields_response_llm = InvalidResponseLLM()
task_recognizer = TaskRecognizer()
field_validator = FieldValidator()
field_inputer = FieldInputer()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chosen_task" not in st.session_state:
    st.session_state.chosen_task = None

if "final_task" not in st.session_state:
    st.session_state.final_task = None

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
    st.session_state.chosen_task = field_inputer.work(
        st.session_state.chosen_task, prompt
    )
    invalid_fields = field_validator.work(st.session_state.chosen_task)
    if len(invalid_fields) == 0:
        formatted_answer = final_response_llm.work(st.session_state.chosen_task)
        st.session_state.final_task = st.session_state.chosen_task
        st.session_state.chosen_task = None
    else:
        formatted_answer = invalid_fields_response_llm.work(
            st.session_state.chosen_task, invalid_fields
        )
        st.session_state.chosen_task = field_inputer.work(
            st.session_state.chosen_task, prompt
        )
        st.session_state.final_task = None
    with st.chat_message("assistant"):
        response = st.write_stream(formatted_answer)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.final_task:
    user_task_name = st.text_input("Enter New Task Name:")
    if st.button("Save chosen task."):
        with open(f"app/stored_instances/{user_task_name.lower().replace(' ', '_')}.pkl", "wb") as f:
            pickle.dump(st.session_state.final_task, f)
        st.success("Task saved successfully! <3")
    if st.button("Clear chat"):
        st.session_state.clear()
        st.rerun()
