from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker

class SubsetCreator(BaseSubsetWorker):
    def __init__(self, input_instances, subset_database):
        super().__init__()
        self.subset_database = subset_database
        self.formatted_index_dataset_name = self.subset_database.replace(" ", "_")
        self.input_instances = input_instances

    def work(self):

        self.es_client.indices.create(
            index=self.formatted_index_dataset_name
        )

        idx = 0
        for doc in self.input_instances:
            idx += 1
            self.es_client.index(
                index=self.formatted_index_dataset_name,
                id=idx,
                document=doc["_source"]
            )

        return len(self.input_instances)
