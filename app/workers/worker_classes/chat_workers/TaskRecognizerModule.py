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
            ]

    def work(self, user_prompt):
        chosen_classes = self._find_task(user_prompt)
        chosen_tasks = []
        for c in chosen_classes:
            chosen_tasks.append(c())

        return chosen_tasks

    def _find_task(self, user_prompt):
        prompt_embedd = self.embedding_model.encode(user_prompt).reshape(1, -1)
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
