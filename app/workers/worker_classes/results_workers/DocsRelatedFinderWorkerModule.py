from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import streamlit as st
import pandas as pd

class DocsRelatedFinderWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name, data=None):
        super().work(task_instance, index_name, task_instance.result_count, data=data)

        titles = []
        full_texts = []
        for row in self.final_data:
            titles.append(row.get("title", None))
            full_texts.append(row.pop("text", None))
        df = pd.json_normalize(self.final_data)
        cols = ["score"] + [c for c in df.columns if c != "score"]

        if "score" in df:
            df = df[cols]

            st.dataframe(
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
            )
        else:
            st.write("No related texts found.")
    
    def _create_query(self, task_instance):
        query = {}
        if task_instance.search_type == "more_like_this":
            query = {  
                    "more_like_this": {
                        "fields": [
                            "title",
                            "text"
                        ],
                        "like": task_instance.short_phrase,
                        "min_term_freq": 1,
                        "max_query_terms": 12
                    }
            }
        return query
    
    def _prepare_final_data(self):
        final_data = []
        for doc in self.data:
            single_speech = doc["_source"]
            single_res = {k: single_speech[k] for k in single_speech.keys() if k not in ["unique_hash"]}
            single_res["score"] = doc["_score"]
            final_data.append(single_res)

        return final_data