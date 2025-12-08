from abc import ABC, abstractmethod
import os
import json
from elasticsearch import Elasticsearch
from workers.worker_classes.dataset_workers import SubsetCreator, SubsetDeletor
from workers.worker_classes.chat_workers import DatasetDescriptionGenerator


class ResultsWorker(ABC):
    def __init__(self):
        self.es_client = Elasticsearch('http://localhost:9200')

    @abstractmethod
    def work(self, task_instance, index_name, subset_max_size=10000, data=None):
        self.query = self._create_query(task_instance)
        if not data:
            self.data = self._query_texts(index_name, self.query, subset_max_size)
        else:
            self.data = data
        self.task_instance = task_instance
        self.index_name = index_name

        self.final_data = self._prepare_final_data()

    @abstractmethod
    def _query_texts(self, task_instance, index_name):
        pass

    def _create_subset_dataset(self, new_subset_name):
        subset_creator = SubsetCreator(self.data, new_subset_name)
        subset_deletor = SubsetDeletor(new_subset_name)
        try:
            print("Refreshing your index...")
            subset_deletor.work()
        except:
            print("Creating new index...")
        
        description_generator = DatasetDescriptionGenerator()
        description_generator.work(self.task_instance, self.index_name, new_subset_name)

        return subset_creator.work()
    
    def _query_texts(self, index_name, query, subset_max_size):
        response = self.es_client.search(
            index=index_name,
            query=query,
            size=subset_max_size
        )
        data = []
        for doc in response["hits"]["hits"]:
            data.append(doc)
        return data
    
    @abstractmethod
    def _create_query(self, task_instance):
        pass

    @abstractmethod
    def _prepare_final_data(self):
        pass
