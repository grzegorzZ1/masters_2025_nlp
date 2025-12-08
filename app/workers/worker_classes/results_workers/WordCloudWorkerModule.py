from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st


class WordCloudWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name):
        super().work(task_instance, index_name)
        all_words = []
        for speech in self.data:
            response = self.es_client.indices.analyze(
                body={
                    "tokenizer": "standard",
                    "filter": ["stop"],
                    "text": speech
                }
            )["tokens"]

            for token in response:
                all_words.append(token["token"].lower())
                

        word_frequencies = pd.Series(all_words).value_counts()
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            random_state=42
        ).generate_from_frequencies(word_frequencies)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        
        st.pyplot(fig)

    def _query_texts(self, task_instance, index_name):
        subset_speech_texts = []
        query = {
                    "range": {
                        "date": {
                            "gte": "-".join(task_instance.min_date.split("-")[::-1]),
                            "lte": "-".join(task_instance.max_date.split("-")[::-1])
                        }
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
            subset_speech_texts.append(doc["_source"]["text"])
        
        return subset_speech_texts
