from workers.worker_classes.WorkerModule import Worker
import json
import io


class InvalidResponseLLM(Worker):
    def __init__(self):
        super().__init__()

    def work(self, task_instance, invalid_fields):
        response = f"""
            Based on your prompt you chose task {task_instance.name}. 
            However you need to specify following information to proceed: {str(invalid_fields)}
        """
        stream_response = io.StringIO(response)
        
        for line in stream_response:
            for word in line.split():
                try:
                    yield word + " "
                except json.JSONDecodeError:
                    continue