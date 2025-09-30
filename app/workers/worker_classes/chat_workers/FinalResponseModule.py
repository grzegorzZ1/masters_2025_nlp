from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker
import json


class FinalResponse(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, final_task):
        """
        Stream responses with real-time output
        """

        response = f"Chosen task: **{final_task.name}**.\nTask Parameters:\n"

        for name, value in final_task:
            response += f"* {name}: {value}\n"

        chunk_size = 16
        for i in range(0, len(response), chunk_size):
            yield response[i:i+chunk_size]