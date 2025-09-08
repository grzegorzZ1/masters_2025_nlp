from abc import ABC, abstractmethod
import os
import requests
from pymilvus import Collection


class ResultsWorker(ABC):
    def __init__(self, params):
        self.params = params
        self.collection = Collection("russian_speeches")
        self.collection.load()

    @abstractmethod
    def work(self):
        pass

    def query_texts(self, query_params, output_fields):
        results = self.collection.query(
            expr="year == 2000", output_fields=["year", "month", "day"]
        )
