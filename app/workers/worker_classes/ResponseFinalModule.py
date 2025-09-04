from workers.worker_classes.WorkerModule import Worker
import json


class FinalResponseLLM(Worker):
    def __init__(self):
        super().__init__()
        self.base_prompt = """
            You will be given task object with its parameters.
            Show it to me specifying name of the task and after that show me formatted dictionary of its parameters.
        """

    def work(self, chosen_task):
        """
        Stream responses from Ollama API with real-time output
        """
        whole_prompt = self.base_prompt + "Name: " + chosen_task.name + " . Params: " + chosen_task.model_dump_json()
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


