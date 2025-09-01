from workers.worker_classes.WorkerModule import Worker
import json


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
                    chunk = json.loads(line.decode("utf-8"))
                    if "response" in chunk:
                        yield chunk["response"]

                    if chunk.get("done", False):
                        break

                except json.JSONDecodeError:
                    continue
