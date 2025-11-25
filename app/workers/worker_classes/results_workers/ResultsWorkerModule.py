from abc import ABC, abstractmethod
import os
from elasticsearch import Elasticsearch


class ResultsWorker(ABC):
    def __init__(self):
        self.es_client = Elasticsearch('http://localhost:9200')
        self.subset_max_size = 10000

    @abstractmethod
    def work(self, task_instance, index_name):
        self.data = self._query_texts(task_instance, index_name)

    @abstractmethod
    def _query_texts(self, task_instance, index_name):
        pass
