import streamlit as st
from dotenv import load_dotenv
from workers.worker_classes.chat_workers import (
    TaskChosenResponse,
    TaskRecognizer,
    FieldInputer,
)
import pickle
import time

load_dotenv()

st.set_page_config("Task Recognizer Chat")
st.title("Task Recognizer Chat")
task_chosen_response = TaskChosenResponse()
task_recognizer = TaskRecognizer()
field_inputer = FieldInputer()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_full_context" not in st.session_state:
    st.session_state.user_full_context = []

if "chosen_tasks" not in st.session_state:
    st.session_state.chosen_tasks = None

if "final_task" not in st.session_state:
    st.session_state.final_task = None

if "empty_fields" not in st.session_state:
    st.session_state.empty_fields = []

if "saving_task" not in st.session_state:
    st.session_state.saving_task = False

if not st.session_state.final_task:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_full_context.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.chosen_tasks = task_recognizer.work(str(st.session_state.user_full_context))
        if prompt in ["1", "2", "3"]:
            st.session_state.final_task = st.session_state.chosen_tasks[int(prompt)-1]
            formatted_answer = f"""
**Chosen task:** {st.session_state.final_task.name}\n
**Task Description:** {st.session_state.final_task.description}\n
You can now either save your task with specified parameters or refresh the chat to select another one.
"""
        else:
            formatted_answer = task_chosen_response.work(st.session_state.chosen_tasks)
        with st.chat_message("assistant"):
            st.write(formatted_answer)

        st.session_state.messages.append({"role": "assistant", "content": formatted_answer})

if st.session_state.final_task and not st.session_state.saving_task:
    if st.button("Refresh chat"):
        st.session_state.final_task = None
        st.session_state.messages = []
        st.session_state.user_full_context = []
        st.rerun()
    if st.button("Proceed to saving task"):
        st.session_state.saving_task = True
        st.rerun()

if st.session_state.saving_task:
    st.write(f"Chosen task: **{st.session_state.final_task.name}**")
    field_values = field_inputer.work(st.session_state.final_task)
    
    field_values_complete = True
    for name, value in field_values.items():
        if value == "":
            field_values_complete = False

    if field_values_complete:
        st.session_state.final_task = type(st.session_state.final_task)(**field_values)
        user_task_name = st.text_input("Enter New Task Name:")
        if st.button("Save chosen task"):
            with open(f"app/stored_instances/{user_task_name.lower().replace(' ', '_')}.pkl", "wb") as f:
                pickle.dump(st.session_state.final_task, f)
            st.success("Task saved successfully! <3")
        if st.button("Clear chat"):
            st.session_state.clear()
            st.rerun()