import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage

from research_chatbot.graph import ResearchChatbot
from research_chatbot.utils import generate_thread_id

load_dotenv()

st.set_page_config("Research Chatbot")
st.title("Research Chatbot")
research_chatbot = ResearchChatbot()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(AIMessage(content="""
Hello! I'm your research assistant. 🎓🤖\n
Please define your research questions — the more precise, the better answers I can provide.
Together we'll refine the research problem and produce answers based on your document base. ✨
"""
))

for message in st.session_state.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

if prompt := st.chat_input("Ask me anything about research..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    response = research_chatbot.work(st.session_state.messages, thread_id=st.session_state.thread_id)
    st.session_state.messages.append(AIMessage(content=response))
    with st.chat_message("assistant"):
        st.markdown(response)

if st.button("Clear Chat"):
    st.session_state.pop("thread_id", None)
    st.session_state.pop("messages", None)
    st.rerun()
