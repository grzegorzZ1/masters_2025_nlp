from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker
import json
import io


class InvalidResponse(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, invalid_fields):
        properties = task_instance.model_json_schema()["properties"]
        response = f"You chose task **{task_instance.name.replace('_', ' ').capitalize()}**.\nHowever you need to specify following information to proceed:\n"
        for name, vals in properties.items():
            response += f"""* **{name}**: {vals["description"]}\n"""

        chunk_size = 16
        for i in range(0, len(response), chunk_size):
            yield response[i:i+chunk_size]
