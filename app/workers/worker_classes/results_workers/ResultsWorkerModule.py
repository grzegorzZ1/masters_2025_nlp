from abc import ABC, abstractmethod
import os
import requests
from pymilvus import Collection
from sqlalchemy import create_engine


class ResultsWorker(ABC):
    def __init__(self):
        self.db_engine = create_engine(os.getenv("DATABASE_URL"), echo=False, future=True)

    @abstractmethod
    def work(self, task_instance, dataset_class):
        self.data = self._query_texts(task_instance, dataset_class)

    @abstractmethod
    def _query_texts(self, task_instance, dataset_class):
        pass
