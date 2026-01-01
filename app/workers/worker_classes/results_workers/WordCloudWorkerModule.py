from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st


class WordCloudWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name, data=None):
        super().work(task_instance, index_name, data=data)

        all_words = []
        for speech in self.final_data:
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
        
        df = word_frequencies.reset_index()
        df.columns = ['Term', 'Frequency']
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=600,
        )

    def _create_query(self, task_instance):
        query = {
                    "range": {
                        "date": {
                            "gte": "-".join(task_instance.min_date.split("-")[::-1]),
                            "lte": "-".join(task_instance.max_date.split("-")[::-1])
                        }
                    }
                }
        return query

    def _prepare_final_data(self):
        final_data = []
        for doc in self.data:
            final_data.append(doc["_source"]["text"])
        
        return final_data