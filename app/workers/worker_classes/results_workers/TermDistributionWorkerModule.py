from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker
from pymilvus import connections


class TermDistributionWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self):
        return super().work()
