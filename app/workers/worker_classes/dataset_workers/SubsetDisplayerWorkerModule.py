import streamlit as st
import pandas as pd

from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker

class SubsetDisplayer(BaseSubsetWorker):
    def __init__(self):
        super().__init__()
    
    def work(self, titles, full_texts, final_data):
        df = pd.json_normalize(final_data)

        cols = ["score"] + [c for c in df.columns if c != "score"]
        df = df[cols]

        selected_row = st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "score": st.column_config.NumberColumn(
                    "Score",
                    format="%.3f",
                    width="small",
                ),
                "date": st.column_config.DatetimeColumn(
                    "Date",
                    format="YYYY-MM-DD HH:mm",
                    width="small",
                ),
                "title": st.column_config.TextColumn(
                    "Title",
                    width="large",
                ),
            },
            height=600,
            on_select="rerun",
            selection_mode="single-row",
        )
        if selected_row["selection"]["rows"]:
            idx = selected_row["selection"]["rows"][0]
            st.write(f"**{titles[idx]}**")
            st.write(full_texts[idx])
    