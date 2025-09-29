from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker
import json


class FinalResponseLLM(ChatWorker):
    def __init__(self):
        super().__init__()
        self.base_prompt = """
            You will be given list of task objects with their descriptions.
            Show it to me as an ordered list of tasks including task name and description.
        """

    def work(self, chosen_tasks):
        """
        Stream responses from Ollama API with real-time output
        """
        whole_prompt = self.base_prompt
        for task in chosen_tasks:
            whole_prompt = (
                whole_prompt
                + "Name: "
                + task.name
                + ". Description: "
                + task.description
            )
        response = self._ollama_request(whole_prompt)

        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if "response" in chunk:
                        yield chunk["response"]

                    if chunk.get("done", False):
                        break

                except json.JSONDecodeError:
                    continue
