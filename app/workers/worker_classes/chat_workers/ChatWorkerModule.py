from abc import ABC, abstractmethod
import os
import requests


class ChatWorker(ABC):
    @abstractmethod
    def work(self):
        pass

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
                current_llama_uri, json=payload, stream=is_stream, timeout=60
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return
