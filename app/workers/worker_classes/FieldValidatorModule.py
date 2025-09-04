from workers.worker_classes.WorkerModule import Worker

class FieldValidator(Worker):
    def __init__(self):
        super().__init__()
    
    def work(self, task_instance):
        invalid_fields = []
        for name, field in task_instance:
            if not field:
                invalid_fields.append(name)
        return invalid_fields