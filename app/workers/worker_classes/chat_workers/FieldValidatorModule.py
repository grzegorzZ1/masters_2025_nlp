from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker


class FieldValidator(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance):
        invalid_fields = []
        for name, field in task_instance:
            if not field:
                invalid_fields.append(name)
        return invalid_fields
