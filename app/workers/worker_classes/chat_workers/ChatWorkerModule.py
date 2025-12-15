from abc import ABC, abstractmethod

from workers.utils.func_utils import ollama_request


class ChatWorker(ABC):
    @abstractmethod
    def work(self):
        pass

    def _ollama_request(self, prompt, is_stream=True):
        ollama_request(prompt, is_stream)
