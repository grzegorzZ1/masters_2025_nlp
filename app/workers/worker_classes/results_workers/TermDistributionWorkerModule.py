from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime


class TermDistributionWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name):
        super().work(task_instance, index_name)
        appear_counts = {}
        docs_counts = {}
        for word in task_instance.terms.split(","):
            appear_counts[word] = {}
            docs_counts[word] = {}

            for key, val in self.data.items():
                appear_counts[word][key] = val.lower().split().count(word.lower())

                counts = 0
                for doc in val.split("[END]"):
                    if word in doc.lower():
                        counts += 1
                docs_counts[word][key] = counts
        
        date_regex = ""
        if task_instance.granularity == "day":
            date_regex = "%Y-%m-%d"
        if task_instance.granularity == "month":
            date_regex = "%Y-%m"
        if task_instance.granularity == "year":
            date_regex = "%Y"

        fig, ax = plt.subplots(figsize=(10, 5))

        for word in task_instance.terms.split(","):
            sorted_items = sorted(appear_counts[word].items(), key=lambda x: datetime.strptime(x[0], date_regex))
            dates = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]

            ax.plot(dates, values, label=word)

        ax.set_title("Monthly Values Plot")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.legend()
        ax.tick_params(axis="x", rotation=45)
        
        st.pyplot(fig)
    
    def _query_texts(self, task_instance, index_name):
        subset_speech_texts = {}

        terms_list = []
        for word in task_instance.terms.split(","):
            terms_list.append({"match": {"text": word}})

        query = {
            "bool": {
                "must": [
                    {
                        "range": {
                            "date": {
                                "gte": "-".join(task_instance.min_date.split("-")[::-1]),
                                "lte": "-".join(task_instance.max_date.split("-")[::-1])
                            }
                        }
                    },
                    {
                        "bool": {
                            "should": terms_list,
                            "minimum_should_match": 1
                        }
                    }
                ]
            }
        }

        response = self.es_client.search(
            index=index_name,
            query=query,
            size=self.subset_max_size
        )
        for doc in response["hits"]["hits"]:
            doc_date = doc["_source"]["date"].split("T")[0]
            if task_instance.granularity == "month":
                doc_date = "-".join(doc_date.split("-")[:2])
            if task_instance.granularity == "year":
                doc_date = doc_date.split("-")[0]
            if doc_date not in subset_speech_texts:
                subset_speech_texts[doc_date] = doc["_source"]["text"]
            else:
                subset_speech_texts[doc_date] = subset_speech_texts[doc_date] + " [END] " + doc["_source"]["text"]
        
        return subset_speech_texts
