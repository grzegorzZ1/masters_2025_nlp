from workers.worker_classes.WorkerModule import Worker
from workers.utils.task_definitions import *
import json


class FieldInputer(Worker):
    def __init__(self):
        super().__init__()
    
    def work(self, task_instance, user_prompt):
        task_updated_fields = {}
        task_descriptions = {}
        for name, field in type(task_instance).model_fields.items():
            task_descriptions[name] = field.description
        
        for name, field in task_instance:
            if not field:
                llm_response = self._extract_single_field(
                    name,
                    user_prompt,
                    task_descriptions[name]
                ).replace(" ", "")
                final_response = json.loads(llm_response)
                if final_response[name] == "ERROR":
                    task_updated_fields[name] = None
                else:
                    task_updated_fields[name] = final_response[name]
            else:
                task_updated_fields[name] = field
        
        return type(task_instance)(**task_updated_fields)
    
    def _extract_single_field(self, parameter_name, user_prompt, field_description):
        prompt = f"""
            Extract value of parameter: {parameter_name} from it.
            Additional information about this parameter is: {field_description}.
            Remember to format parameter value to proper format based on description 
            User prompt is: {user_prompt}.
            Format of your answer should be ONLY dictionary without any other text:
        """ + """{PARAM_NAME: PARAM_VALUE}. If can not find it return "ERROR" as PARAM VALUE."""
        response = self._ollama_request(prompt, is_stream=False)

        return response.json()["response"]
