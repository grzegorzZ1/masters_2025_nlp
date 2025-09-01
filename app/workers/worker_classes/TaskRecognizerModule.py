from workers.worker_classes.WorkerModule import Worker
from sklearn.metrics.pairwise import cosine_similarity
from workers.utils.task_definitions import *
import numpy as np
from sentence_transformers import SentenceTransformer


class TaskRecognizer(Worker):
    def __init__(self):
        super().__init__()
        self.embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
        with open("app/workers/utils/task_definitions/embeddings.json", "r") as file:
            self.task_classes = [
                TermDistribution,
                WordCloud,
            ]

    def work(self, user_prompt):
        chosen_task = self._find_task(user_prompt)
        date_range = self._find_date_range(user_prompt)

        return chosen_task, date_range

    def _find_task(self, user_prompt):
        prompt_embedd = self.embedding_model.encode(user_prompt).reshape(1, -1)
        task_names = []
        cosine_similarities = []

        for task_class in self.task_definition:
            task_names.append(task_class)
            cosine_similarities.append(
                cosine_similarity(
                    np.array(task_class().embedding).reshape(1, -1), prompt_embedd
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
