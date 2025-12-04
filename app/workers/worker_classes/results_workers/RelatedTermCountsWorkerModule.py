from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker


class RelatedTermCountsWorker(ResultsWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name):
        super().work(task_instance, index_name)
    
    def _query_texts(self, task_instance, index_name):
        pass