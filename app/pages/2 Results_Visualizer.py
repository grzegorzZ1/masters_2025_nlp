import streamlit as st
import os
import pickle

st.set_page_config("Results Visuzalizer")
st.title("Results Visuzalizer.")

if "final_task" not in st.session_state:
    st.session_state.final_task = None
if "visualization_params" not in st.session_state:
    st.session_state.visualization_params = {}

folder_path = "app/stored_instances"  
files = os.listdir(folder_path)
files = [file[:-4] for file in files if not "init" in file]

selected_task = st.selectbox("Choose a task:", files)
file_path = os.path.join(folder_path, selected_task)

if st.button("Load task"):
    with open(f"{file_path}.pkl", "rb") as f:
        st.session_state.final_task = pickle.load(f)
if st.button("Delete task"):
    os.remove(f"{file_path}.pkl")
    st.session_state.clear()
    st.rerun()

if st.session_state.final_task:
    st.subheader(f"Chosen task: {st.session_state.final_task.name.replace('_', ' ').capitalize()}")

    for key, value in st.session_state.final_task:
        description = type(st.session_state.final_task).model_fields[key].description
        st.session_state.visualization_params[key] = st.text_input(key, value=value, help=description)

    results_worker = st.session_state.final_task.vizualization_worker()
    st.session_state.final_task = type(st.session_state.final_task)(**st.session_state.visualization_params)
    results_worker.work(st.session_state.final_task)

    with st.expander("Create new task"):
        user_task_name = st.text_input("Enter New Task Name:")
        
        if st.button("Submit"):
            if user_task_name:
                file_path = os.path.join(folder_path, user_task_name)
                with open(f"{file_path}.pkl", "wb") as f:
                    pickle.dump(
                        type(st.session_state.final_task)(**st.session_state.visualization_params),
                        f
                    )
                st.success("Task created!")
                st.rerun()
            else:
                st.warning("Please provide a unique name for new task.")
