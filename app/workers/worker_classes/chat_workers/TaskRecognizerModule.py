from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker
from sklearn.metrics.pairwise import cosine_similarity
from workers.utils.task_definitions import *
import numpy as np
import os
from sentence_transformers import SentenceTransformer


class TaskRecognizer(ChatWorker):
    def __init__(self):
        super().__init__()
        self.embedding_model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
        with open("app/workers/utils/task_definitions/embeddings.json", "r") as file:
            self.task_classes = [
                TermDistribution,
                WordCloud,
                RelationFinder,
                RelatedTermCounts,
                DocsRelatedFinder
            ]

    def work(self, user_prompt):
        chosen_classes = self._find_task(user_prompt)
        chosen_tasks = []
        for c in chosen_classes:
            chosen_tasks.append(c())

        return chosen_tasks

    def _find_task(self, user_prompt):
        filtered_decription = self._task_description_from_prompt(user_prompt)
        prompt_embedd = self.embedding_model.encode(filtered_decription).reshape(1, -1)
        task_names = []
        cosine_similarities = []

        for task_class in self.task_classes:
            task_names.append(task_class)
            cosine_similarities.append(
                cosine_similarity(
                    np.array(task_class().embedding).reshape(1, -1), prompt_embedd
                )[0]
            )
        cosine_similarities = np.array(cosine_similarities).reshape(1, -1)[0]
        task_names = np.array(task_names)[np.argsort(cosine_similarities)][::-1]
        return task_names[:3]

    def _task_description_from_prompt(self, user_prompt):
        prompt = f"""
You will be given a description of a text analytical task provided by the user.
Provide short (max 2 sentences) description of this task without mentioning its parameters which user might provide, just overall overview of the task.
User prompt is: {user_prompt}
Your answer should contain just the description without any additions.
"""
        return self._ollama_request(prompt, is_stream=False)
