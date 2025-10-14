import streamlit as st
import datetime
from workers.worker_classes.dataset_workers import SubsetCreator, FilterDetector
from workers.worker_classes.chat_workers import DatasetFilterResponse

st.set_page_config("Dataset Creation")
st.title("Dataset Creation")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chosen_filters" not in st.session_state:
    st.session_state.chosen_filters = {}

if "user_full_context" not in st.session_state:
    st.session_state.user_full_context = []

filter_detector = FilterDetector()
filter_response = DatasetFilterResponse()

base_dataset_name = st.selectbox("Choose a base dastaset:", ["speech"])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_full_context.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chosen_filters = filter_detector.work(st.session_state.user_full_context)
    formatted_answer = filter_response.work(st.session_state.chosen_filters)
    
    with st.chat_message("assistant"):
        response = st.write_stream(formatted_answer)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.chosen_filters != {}:
    subset_name = st.text_input("Enter new dataset name:")
    if st.button("Create dataset with selected filters"):
        for i in range(10):
            try:
                subset_creator_worker = SubsetCreator(st.session_state.chosen_filters, base_dataset_name, subset_name)
                filtered_speeches_count = subset_creator_worker.work()
                st.write(f"Created subset dataset with: {filtered_speeches_count} observations.")
                break
            except AttributeError:
                continue
if st.button("Clear chat"):
    st.session_state.clear()
    st.rerun()
