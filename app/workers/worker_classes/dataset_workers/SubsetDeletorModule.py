import os
import json
from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker


class SubsetDeletor(BaseSubsetWorker):
    def __init__(self, subset_database):
        super().__init__()
        self.subset_database = subset_database

    def work(self):

        description_file_path = f"app/{os.getenv('DATASET_DESCRIPTIONS')}"
        with open(description_file_path, "r") as f:
            descriptions = json.load(f)

        descriptions.pop(self.subset_database, None)

        with open(description_file_path, 'w') as f:
            json.dump(descriptions, f)

        self.es_client.indices.delete(index=self.subset_database)