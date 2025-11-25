from workers.worker_classes.results_workers.ResultsWorkerModule import ResultsWorker


class RelationFinderWorker(ResultsWorker):
    def __init__(self):
        super().__init__()
        self.output_fields = ["year", "month", "day", "words"]

    def work(self, task_instance, index_name):
        super().work(task_instance, index_name)
    
    def _query_texts(self, task_instance, index_name):
        pass