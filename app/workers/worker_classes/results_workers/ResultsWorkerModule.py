from abc import ABC, abstractmethod
import os
import json
import requests
from elasticsearch import Elasticsearch

from workers.utils.func_utils import ollama_request
from workers.worker_classes.dataset_workers import SubsetCreator, SubsetDeletor


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
        
        self._generate_dataset_description(self.task_instance, self.index_name, new_subset_name)

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

    def _generate_dataset_description(self, task_instance, index_name, new_subset_name):
        task_field_values = json.loads(task_instance.model_dump_json())
        task_name = type(task_instance).name
        task_description = type(task_instance).description
        task_field_descriptions = {}
        for name, value in type(task_instance).model_fields.items():
            if not value.default:
                task_field_descriptions[name] = value.description
        
        description_file_path = f"app/{os.getenv('DATASET_DESCRIPTIONS')}"
        with open(description_file_path, "r") as f:
            descriptions = json.load(f)
        current_description = descriptions[index_name].copy()
        
        new_description = self._generate_description(task_field_values, task_name, task_description, task_field_descriptions)
        current_description.append(new_description)

        descriptions[new_subset_name] = current_description

        with open(description_file_path, 'w') as f:
            json.dump(descriptions, f)

        
    def _generate_description(self, task_field_values, task_name, task_description, task_field_descriptions):
        prompt = f"""
You will be given a NLP task. In answer write task name and IN ONE SENTENCE describe a dataset which was created using filters from this task:
Task Name is: {task_name} (do not change it in answer).
Fields for this task are as follows:
"""
        for key, val in task_field_values.items():
            if key in task_field_descriptions:
                field_description = f"Field name: {key}, Field value: {val}, Field description: {task_field_descriptions[key]}"
                prompt = prompt + f"/n{field_description}"

        response = ollama_request(prompt, is_stream=False)
        return response.json()["response"]
