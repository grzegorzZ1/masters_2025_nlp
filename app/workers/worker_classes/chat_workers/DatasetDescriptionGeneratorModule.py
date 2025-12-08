import json
import os
from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker


class DatasetDescriptionGenerator(ChatWorker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, index_name, new_subset_name):
        task_field_values = json.loads(task_instance.model_dump_json())
        task_name = type(task_instance).name
        task_description = type(task_instance).description
        task_field_descriptions = {}
        for name, value in type(task_instance).model_fields.items():
            if not value.default:
                task_field_descriptions[name] = value.description
        
        description_file_path = f"app/{os.getenv('DATASET_DESCRIPTIONS')}"
        with open(description_file_path, "r") as f:
            descriptions = json.load(f)
        current_description = descriptions[index_name].copy()
        
        new_description = self._generate_description(task_field_values, task_name, task_description, task_field_descriptions)
        current_description.append(new_description)

        descriptions[new_subset_name] = current_description

        with open(description_file_path, 'w') as f:
            json.dump(descriptions, f)

        
    def _generate_description(self, task_field_values, task_name, task_description, task_field_descriptions):
        prompt = f"""
You will be given a NLP task. In answer write task name and IN ONE SENTENCE describe a dataset which was created using filters from this task:
Task Name is: {task_name} (do not change it in answer).
Fields for this task are as follows:
"""
        for key, val in task_field_values.items():
            if key in task_field_descriptions:
                field_description = f"Field name: {key}, Field value: {val}, Field description: {task_field_descriptions[key]}"
                prompt = prompt + f"/n{field_description}"

        response = self._ollama_request(prompt, is_stream=False)
        return response.json()["response"]
