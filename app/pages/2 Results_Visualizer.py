import streamlit as st
import time
import os
import pickle
import json
from workers.worker_classes.dataset_workers import SubsetDeletor
from elasticsearch import Elasticsearch
from typing import _LiteralGenericAlias

es_client = Elasticsearch('http://localhost:9200')

st.set_page_config("Results Visuzalizer")
st.title("Results Visuzalizer")

if "final_task" not in st.session_state:
    st.session_state.final_task = None
if "visualization_params" not in st.session_state:
    st.session_state.visualization_params = {}
if "final_dataset" not in st.session_state:
    st.session_state.final_dataset = None

folder_path = "app/stored_instances"
files = os.listdir(folder_path)
files = [file[:-4] for file in files if not "init" in file]

indices = []
for ind in es_client.cat.indices(format="json"):
    indices.append(ind["index"])

col1, col2 = st.columns(2)

with col1:
    selected_task = st.selectbox("Choose a task:", files)
    file_path = os.path.join(folder_path, selected_task)
    if st.button("Load task"):
        with open(f"{file_path}.pkl", "rb") as f:
            st.session_state.final_task = pickle.load(f)
        st.write(f"Task **{st.session_state.final_task.name}** chosen ✅")
    if st.button("Delete task"):
        os.remove(f"{file_path}.pkl")
        st.session_state.clear()
        st.rerun()

with col2:
    chosen_dataset = st.selectbox(
        "Choose a dataset:",
        indices
    )
    if st.button("Choose dataset"):
        st.session_state.final_dataset = chosen_dataset
    if st.session_state.final_dataset:
        st.write(f"Dataset **{st.session_state.final_dataset}** loaded ✅")
        with st.expander("Dataset description"):
            print(os.getcwd())
            description_file_path = f"app/{os.getenv('DATASET_DESCRIPTIONS')}"
            with open(description_file_path, "r") as f:
                descriptions = json.load(f)
            
            st.write(descriptions[st.session_state.final_dataset])
        if st.button("Delete dataset"):
            subset_deletor = SubsetDeletor(st.session_state.final_dataset)
            subset_deletor.work()
            st.session_state.clear()
            st.rerun()
if st.session_state.final_task:
    st.subheader(f"Chosen task: {st.session_state.final_task.name.replace('_', ' ').capitalize()}")

    for key, value in st.session_state.final_task:
        print(key)
        field = type(st.session_state.final_task).model_fields[key]
        description = field.description
        if type(field.annotation) == _LiteralGenericAlias:
            st.session_state.visualization_params[key] = st.selectbox(key, options=field.annotation.__dict__["__args__"], help=description)
        else:
            st.session_state.visualization_params[key] = st.text_input(key, value=value, help=description)
if st.session_state.final_task and st.session_state.final_dataset:
    results_worker = st.session_state.final_task.vizualization_worker()
    st.session_state.final_task = type(st.session_state.final_task)(**st.session_state.visualization_params)
    results_worker.work(st.session_state.final_task, st.session_state.final_dataset)

    with st.expander("Create new task"):
        user_task_name = st.text_input("Enter New Task Name:")
        
        if st.button("Submit", key=1111):
            if user_task_name:
                task_file_path = os.path.join(folder_path, user_task_name)
                with open(f"{task_file_path}.pkl", "wb") as f:
                    pickle.dump(
                        st.session_state.final_task,
                        f
                    )
                st.success("Task created!")
                st.rerun()
            else:
                st.warning("Please provide a unique name for new task.")

    with st.expander("Create new subset"):
        user_subset_name = st.text_input("Enter New Subset Name:")
        
        if st.button("Submit", key=2222):
            if user_subset_name:
                subset_len = results_worker._create_subset_dataset(user_subset_name)
                st.success(f"Subset with {subset_len} observations created!")
                time.sleep(3)
                st.rerun()
            else:
                st.warning("Please provide a unique name for new subset.")
