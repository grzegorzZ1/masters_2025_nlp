import streamlit as st
from dotenv import load_dotenv
import json
from workers.worker_classes.chat_workers import *
import pickle

load_dotenv()

st.set_page_config("Task Recognizer Chat")
st.title("Task Recognizer Chat")
task_chosen_response = TaskChosenResponse()
invalid_fields_response_llm = InvalidResponse()
task_recognizer = TaskRecognizer()
field_validator = FieldValidator()
field_inputer = FieldInputer()
final_response = FinalResponse()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_full_context" not in st.session_state:
    st.session_state.user_full_context = []

if "chosen_tasks" not in st.session_state:
    st.session_state.chosen_tasks = None

if "final_task" not in st.session_state:
    st.session_state.final_task = None

if "invalid_fields" not in st.session_state:
    st.session_state.invalid_fields = ["PLACEHOLDER"]

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
    st.session_state.user_full_context.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not st.session_state.final_task:
        st.session_state.chosen_tasks = task_recognizer.work(str(st.session_state.user_full_context))
        if prompt in ["1", "2", "3"]:
            st.session_state.final_task = st.session_state.chosen_tasks[int(prompt)-1]
        else:
            formatted_answer = task_chosen_response.work(st.session_state.chosen_tasks)
        
    if st.session_state.final_task:
        st.session_state.invalid_fields = field_validator.work(st.session_state.final_task)
        if len(st.session_state.invalid_fields) == 0:
            formatted_answer = final_response.work(st.session_state.final_task)
        else:
            formatted_answer = invalid_fields_response_llm.work(
                st.session_state.final_task, st.session_state.invalid_fields
            )
            print(prompt)
            st.session_state.final_task = field_inputer.work(
                st.session_state.final_task, prompt
            )
    
    with st.chat_message("assistant"):
        response = st.write_stream(formatted_answer)
    st.session_state.messages.append({"role": "assistant", "content": response})

if len(st.session_state.invalid_fields) == 0:
    user_task_name = st.text_input("Enter New Task Name:")
    if st.button("Save chosen task."):
        with open(f"app/stored_instances/{user_task_name.lower().replace(' ', '_')}.pkl", "wb") as f:
            pickle.dump(st.session_state.final_task, f)
        st.success("Task saved successfully! <3")
    if st.button("Clear chat"):
        st.session_state.clear()
        st.rerun()