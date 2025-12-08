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

        fig, ax = plt.subplots(2, 1, figsize=(10, 10))
        plt.subplots_adjust(hspace=0.5)

        for word in task_instance.terms.split(","):
            sorted_items_appear = sorted(appear_counts[word].items(), key=lambda x: datetime.strptime(x[0], date_regex))
            dates_appear = [item[0] for item in sorted_items_appear]
            values_appear = [item[1] for item in sorted_items_appear]
            ax[0].plot(dates_appear, values_appear, label=word)

            sorted_items_docs = sorted(docs_counts[word].items(), key=lambda x: datetime.strptime(x[0], date_regex))
            dates_docs = [item[0] for item in sorted_items_docs]
            values_docs = [item[1] for item in sorted_items_docs]

            ax[1].plot(dates_docs, values_docs, label=word)

        ax[0].set_title("Monthly Appear Count")
        ax[0].set_xlabel("Date")
        ax[0].set_ylabel("Apear Count")
        ax[0].legend()
        ax[0].tick_params(axis="x", rotation=45)
        

        ax[1].set_title("Monthly Document Count in Which Word Appeared")
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("Documents Count")
        ax[1].legend()
        ax[1].tick_params(axis="x", rotation=45)

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
        self.instances_for_new_subset = []
        for doc in response["hits"]["hits"]:
            self.instances_for_new_subset.append(doc)
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
