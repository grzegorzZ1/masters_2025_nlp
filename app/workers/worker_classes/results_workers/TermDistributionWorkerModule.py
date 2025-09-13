from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
from pymilvus import connections
from sqlalchemy.orm import Session


class TermDistributionWorker(ResultsWorker):
    def __init__(self):
        super().__init__()
        self.output_fields = ["year", "month", "day", "words"]

    def work(self, task_instance, dataset_class):
        super().work(task_instance, dataset_class)
    
    def _query_texts(self, task_instance, dataset_class):
        pass