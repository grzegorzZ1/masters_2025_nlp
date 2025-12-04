from workers.utils.dataset_filters_definitions import *
import requests
import os
import json

class FilterDetector:
    def __init__(self):
        self.filters = {
            "date": DateFilter,
            "keywords": KeywordFilter,
        }
        self.base_prompt = """

        """

    def work(self, user_prompt):
        chosen_filters = self._choose_filters(user_prompt)
        final_filters = {}
        for key, filter in chosen_filters.items():
            final_filters[key] = self._populate_filter(filter, user_prompt)

        return final_filters

    def _choose_filters(self, user_prompt):
        chosen_filters = {}
        for key, filter in self.filters.items():
            filter_check_prompt = f"""You will be given user prompt and description of a dataset filter.
            You have to specify based on user prompt whether user wants to utilize given filter.
            Answer format (must be a single word):
            - YES if filter description matches users prompt
            - NO in ther cases.

            User prompt: {user_prompt}
            Filter description: {filter.description}
            """

            filter_check = self._ollama_request(filter_check_prompt, is_stream=False).json()["response"]
            if filter_check.replace(" ", "") == "YES":
                chosen_filters[key] = filter()
        
        return chosen_filters

    def _populate_filter(self, filter, user_prompt):
        filter_updated_fields = {}
        param_descriptions = {}
        for name, field in type(filter).model_fields.items():
            param_descriptions[name] = field.description

        for name, field in filter:
            llm_response = self._extract_single_field(
                name, user_prompt, param_descriptions[name]
            ).replace(" ", "")
            try:
                final_response = json.loads(llm_response)
                if final_response[name] == "ERROR":
                    filter_updated_fields[name] = None
                else:
                    filter_updated_fields[name] = final_response[name]
            except:
                filter_updated_fields[name] = None

        return type(filter)(**filter_updated_fields)
    
    def _extract_single_field(self, parameter_name, user_prompt, field_description):
        prompt = (
            f"""
            Extract value of parameter: {parameter_name} from it.
            Additional information about this parameter is: {field_description}.
            Remember to format parameter value to proper format based on description 
            User prompt is: {user_prompt}.
            Format of your answer should be ONLY dictionary without any other text:
        """
            + """{PARAM_NAME: PARAM_VALUE}. If can not find it return "ERROR" as PARAM VALUE."""
        )
        response = self._ollama_request(prompt, is_stream=False)

        return response.json()["response"]

    def _ollama_request(self, prompt, is_stream=True):
        payload = {
            "model": os.getenv("MODEL_NAME"),
            "prompt": prompt,
            "stream": is_stream,
        }
        if os.getenv("IS_IN_DOCKER", False):
            current_llama_host = os.getenv("DOCKER_LLAMA_HOST")
        else:
            current_llama_host = os.getenv("LOCAL_LLAMA_HOST")

        current_llama_uri = current_llama_host + "/api/generate"

        try:
            response = requests.post(
                current_llama_uri, json=payload, stream=is_stream
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return