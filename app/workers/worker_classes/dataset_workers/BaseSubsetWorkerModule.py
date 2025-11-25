from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch

class BaseSubsetWorker(ABC):
    def __init__(self):
        self.es_client = Elasticsearch('http://localhost:9200')
    
    @abstractmethod
    def work(self):
        pass