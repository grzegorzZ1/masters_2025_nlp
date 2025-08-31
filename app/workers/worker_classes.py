from abc import ABC, abstractmethod
import os
import requests
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass

    def _ollama_request(self, prompt, is_stream=True):
        payload = {
            "model": os.getenv("MODEL_NAME"),
            "prompt": prompt,
            "stream": is_stream
        }
        if os.getenv("IS_IN_DOCKER", False):
            current_llama_host = os.getenv("DOCKER_LLAMA_HOST")
        else:
            current_llama_host = os.getenv("LOCAL_LLAMA_HOST")
        
        current_llama_uri = current_llama_host + "/api/generate"

        try:
            response = requests.post(
                current_llama_uri,
                json=payload, 
                stream=is_stream,
                timeout=60
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return


class TaskRecognizer(Worker):
    def __init__(self):
        super().__init__()
        self.embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
        with open("app/workers/utils/task_finder/tasks.json", 'r') as file:
            self.task_definition = json.load(file)
    
    def work(self, user_prompt):
        chosen_task = self._find_task(user_prompt)
        date_range = self._find_date_range(user_prompt)

        return chosen_task, date_range
    
    def _find_task(self, user_prompt):
        prompt_embedd = self.embedding_model.encode(user_prompt).reshape(1, -1)
        task_names = []
        cosine_similarities = []

        for name, params in self.task_definition.items():
            task_names.append(name)
            cosine_similarities.append(
                cosine_similarity(
                    np.array(params["embedding"]).reshape(1, -1),
                    prompt_embedd 
                )[0]
            )
        cosine_similarities = np.array(cosine_similarities).reshape(1, -1)[0]
        task_names = np.array(task_names)[np.argsort(cosine_similarities)][::-1]
        return task_names[0]
    
    def _find_date_range(self, user_prompt):
        prompt = f"""
            You will be given a message from user who requests to perform a task in NLP field. Define what date range for this task was specified by user and return answer in format: \
            [[day_start, month_start, year_start], [day_end, month_end, year_end]]. User prompt is: {user_prompt}. 
        """
        response = self._ollama_request(prompt, is_stream=False)

        return response.json()["response"]


class ResponseLLM(Worker):
    def __init__(self):
        super().__init__()
        self.base_prompt = "You will be given subject we are talking about and date range of analysis. Write its name and write the formatted date range: "

    def work(self, messages, chosen_task, date_range):
        """
        Stream responses from Ollama API with real-time output
        """
        whole_prompt = self.base_prompt + chosen_task + " " + date_range
        response = self._ollama_request(whole_prompt)
            
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        yield chunk['response']

                    if chunk.get('done', False):
                        break
                        
                except json.JSONDecodeError:
                    continue