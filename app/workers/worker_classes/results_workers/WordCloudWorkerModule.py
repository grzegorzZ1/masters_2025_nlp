from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import nltk
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class WordCloudWorker(ResultsWorker):
    POS_TAG_MAP = {
        "noun": "NN",
        "verb": "VB",
        "adjective": "JJ",
    }

    def __init__(self):
        super().__init__()
        nltk.download("punkt_tab", quiet=True)
        nltk.download("averaged_perceptron_tagger_eng", quiet=True)
        self.embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"), device="cpu")

    def _filter_related_words(self, all_words, focus_term):
        """Keep only words semantically related to focus_term based on similarity distribution."""
        word_freq = pd.Series(all_words).value_counts()
        unique_words = word_freq.index.tolist()

        focus_embedding = self.embedding_model.encode([focus_term])
        word_embeddings = self.embedding_model.encode(unique_words)

        similarities = cosine_similarity(focus_embedding, word_embeddings)[0]

        mean_sim = np.mean(similarities)
        std_sim = np.std(similarities)
        threshold = mean_sim + std_sim

        similarity_map = {w: sim for w, sim in zip(unique_words, similarities) if sim >= threshold}
        filtered_words = [w for w in all_words if w in similarity_map]
        return filtered_words, similarity_map

    def work(self, task_instance, index_name, data=None):
        super().work(task_instance, index_name, data=data)
        
        if self.task_instance.pos_filter and self.task_instance.pos_filter in self.POS_TAG_MAP:
            prefix = self.POS_TAG_MAP[self.task_instance.pos_filter]
            all_words = []
            for speech in self.final_data:
                tokens = nltk.word_tokenize(speech)
                tagged = nltk.pos_tag(tokens)
                for word, tag in tagged:
                    word_lower = word.lower()
                    if tag.startswith(prefix) and word_lower.isalpha():
                        all_words.append(word_lower)
        else:
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
        
        similarity_map = None
        if self.task_instance.focus_term:
            all_words, similarity_map = self._filter_related_words(all_words, self.task_instance.focus_term)

        word_frequencies = pd.Series(all_words).value_counts()
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            random_state=42
        ).generate_from_frequencies(word_frequencies)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        title = ""
        if self.task_instance.focus_term:
            title += f"Focus: '{self.task_instance.focus_term}', "
        if self.task_instance.pos_filter:
            title += f"POS: {self.task_instance.pos_filter}s"
        if self.task_instance.min_date and self.task_instance.max_date:
            title += f"\nDate: {self.task_instance.min_date} to {self.task_instance.max_date}"
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')
        
        st.pyplot(fig)
        
        df = word_frequencies.reset_index()
        df.columns = ['Term', 'Frequency']
        if similarity_map:
            df['Similarity'] = df['Term'].map(similarity_map).round(4)
            df = df.sort_values('Similarity', ascending=False).reset_index(drop=True)
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