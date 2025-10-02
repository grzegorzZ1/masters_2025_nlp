from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker


class DatasetFilterResponse(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, chosen_filters):
        pass
