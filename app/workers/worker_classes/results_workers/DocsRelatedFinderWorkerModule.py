from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import streamlit as st
import pandas as pd

class DocsRelatedFinderWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name):
        super().work(task_instance, index_name)
        full_texts = []
        for row in self.data:
            full_texts.append(row.pop("text", None))
        df = pd.json_normalize(self.data)

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
            st.write(full_texts[idx])
    
    def _query_texts(self, task_instance, index_name):
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

        response = self.es_client.search(
            index=index_name,
            query=query,
            size=min(self.subset_max_size, task_instance.result_count)
        )
        res = []
        self.instances_for_new_subset = []
        for single_hit in response["hits"]["hits"]:
            self.instances_for_new_subset.append(single_hit)
            single_speech = single_hit["_source"]
            single_res = {k: single_speech[k] for k in single_speech.keys() if k not in ["unique_hash"]}
            single_res["score"] = single_hit["_score"]
            res.append(single_res)
        return res