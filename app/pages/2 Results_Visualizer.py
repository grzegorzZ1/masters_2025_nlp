import streamlit as st

#### for test purposes
from workers.utils.task_definitions import *

####
st.set_page_config("Results Visuzalizer")
st.title("Results Visuzalizer.")

if "final_task" not in st.session_state:
    st.session_state.final_task = None
    #### for test purposes
    st.session_state.final_task = WordCloud(
        **{"min_date": "01-01-2020", "max_date": "31-12-2021"}
    )
    ####

if "visualization_params" not in st.session_state:
    st.session_state.visualization_params = {}

st.subheader(f"Chosen task: {st.session_state.final_task.name}")

for key, value in st.session_state.final_task:
    st.session_state.visualization_params[key] = st.text_input(key, value=value)

for key, value in st.session_state.visualization_params.items():
    st.write(key, value)
