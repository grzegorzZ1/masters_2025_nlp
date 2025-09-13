import streamlit as st
import datetime
from workers.worker_classes.dataset_workers import SubsetCreator

st.set_page_config("Dataset Creation")
st.title("Dataset Creation")

st.session_state.final_filters = {}
st.session_state.chosen_filters = {
    "date": False,
    "keywords": False,
    "sentiment": False
}

base_dataset_name = st.selectbox("Choose a base dastaset:", ["speech"])

if st.toggle("Filter by date."):
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.date(2000, 1, 1),
            min_value=datetime.date(1995, 1, 1),
            max_value=datetime.date.today()
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.date.today(),
            min_value=start_date,
            max_value=datetime.date.today()
        )
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    st.session_state.chosen_filters["date"] = True

if st.toggle("Filter by keywords."):
    if "keyword_tags" not in st.session_state:
        st.session_state.keyword_tags = []

    new_tag = st.text_input("Enter a word and press Add:", key="tag_text_add")

    if st.button("Add", key="tag_add") and new_tag:
        if new_tag not in st.session_state.keyword_tags:
            st.session_state.keyword_tags.append(new_tag)
        st.session_state.new_tag = ""

    st.write("Your keywords:")

    for i, tag in enumerate(st.session_state.keyword_tags):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"- **{tag}**")
        with col2:
            if st.button("❌", key=f"del_tag_{i}"):
                st.session_state.keyword_tags.pop(i)
                st.rerun()
    
    st.session_state.chosen_filters["keywords"] = True

if st.toggle("Filter by Sentiment."):
    if "sentiment_tags" not in st.session_state:
        st.session_state.sentiment_tags = {}

    col1, col2 = st.columns([5, 1])
    with col1:
        new_tag = st.text_input("Enter a word and press Add:", key="sentiment_text_add")
    with col2:
        choice = st.selectbox("Chose Sentiment:", ["Positive", "Negative"])
    

    if st.button("Add", key="sentiment_add") and new_tag:
        if new_tag not in st.session_state.sentiment_tags:
            st.session_state.sentiment_tags[new_tag] = choice
        st.session_state.new_tag = ""

    st.write("Your Tags:")

    for tag in st.session_state.sentiment_tags:
        col1, col2 = st.columns([5, 1])
        with col1:
            color = "green" if st.session_state.sentiment_tags[tag] == "Positive" else "red"
            st.markdown(
                f"<span style='color:{color}; font-weight:bold;'>• {tag}</span>",
                unsafe_allow_html=True
            )
        with col2:
            if st.button("❌", key=f"del_sent_{tag}"):
                st.session_state.sentiment_tags.pop(tag, None)
                st.rerun()
    
    st.session_state.chosen_filters["sentiment"] = True


with st.popover("Create dataset with selected filters"):
    if st.session_state.chosen_filters["date"]:
        st.session_state.final_filters["date"] = {}
        st.session_state.final_filters["date"]["min_date"] = start_date
        st.session_state.final_filters["date"]["max_date"] = end_date
    if st.session_state.chosen_filters["keywords"]:
        st.session_state.final_filters["keywords"] = st.session_state.keyword_tags
    if st.session_state.chosen_filters["sentiment"]:
        st.session_state.final_filters["sentiment"] = st.session_state.sentiment_tags
    subset_name = st.text_input("Enter new dataset name:")
    if st.button("Submit"):
        while True:
            try:
                subset_creator_worker = SubsetCreator(st.session_state.final_filters, base_dataset_name, subset_name)
                filtered_speeches_count = subset_creator_worker.work()
                st.write(f"Created subset dataset with: {filtered_speeches_count} observations.")
                break
            except:
                continue
