from workers.utils.func_utils import ollama_request
from uuid import uuid4

def generate_thread_id() -> str:
    return str(uuid4())

from uuid import uuid4
import requests
import os

def ollama_request(prompt, is_stream=False):
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
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None