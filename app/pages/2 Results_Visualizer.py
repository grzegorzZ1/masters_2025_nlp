import streamlit as st

st.set_page_config("Results Visuzalizer")
st.title("Results Visuzalizer.")

if "final_task" not in st.session_state:
    st.session_state.final_task = None

if "visualization_params" not in st.session_state:
    st.session_state.visualization_params = {}

for key, value in st.session_state.final_task:
    st.session_state.visualization_params[key] = st.text_input(key, value=value)

for key, value in st.session_state.visualization_params.items():
    st.write(key, value)