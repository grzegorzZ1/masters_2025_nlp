from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker


class SubsetDeletor(BaseSubsetWorker):
    def __init__(self, subset_database):
        super().__init__()
        self.subset_database = subset_database

    def work(self):
        self.es_client.indices.delete(index=self.subset_database)