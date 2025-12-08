from abc import ABC, abstractmethod
import os
from elasticsearch import Elasticsearch
from workers.worker_classes.dataset_workers import SubsetCreator, SubsetDeletor


class ResultsWorker(ABC):
    def __init__(self):
        self.es_client = Elasticsearch('http://localhost:9200')
        self.subset_max_size = 10000
        self.instances_for_new_subset = []

    @abstractmethod
    def work(self, task_instance, index_name):
        self.data = self._query_texts(task_instance, index_name)

    @abstractmethod
    def _query_texts(self, task_instance, index_name):
        pass

    def _create_subset_dataset(self, new_subset_name):
        subset_creator = SubsetCreator(self.instances_for_new_subset, new_subset_name, self.subset_max_size)
        subset_deletor = SubsetDeletor(new_subset_name)
        try:
            print("Refreshing your index...")
            subset_deletor.work()
        except:
            print("Creating new index...")
        
        return subset_creator.work()
