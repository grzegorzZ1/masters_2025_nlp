from abc import ABC, abstractmethod
import os
import requests
import json

def stream_ollama_response(prompt):
    """
    Stream responses from Ollama API with real-time output
    """
    
    payload = {
        "model": os.getenv("MODEL_NAME"),
        "prompt": prompt,
        "stream": True
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
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
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
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

class AbstractWorker(ABC):

    @abstractmethod
    def process_task(self):
        pass