from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import json
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Date, Text, ARRAY, select, and_, or_
from datetime import datetime
from database_utils.utils import Speech


class WordCloudWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, dataset_class):
        super().work(task_instance, dataset_class)
        self.dataset_class = dataset_class
        all_words = []
        for speech in self.data:
            all_words += speech.words

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
    
    def _query_texts(self, task_instance, dataset_class):
        with Session(self.db_engine) as s:
            start = datetime.strptime(task_instance.min_date, "%d-%M-%Y").date()
            end = datetime.strptime(task_instance.max_date, "%d-%M-%Y").date()

            stmt = (
                select(dataset_class)
                .where(dataset_class.doc_date.between(start, end))
            )

            return s.execute(stmt).scalars().all()


