from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker


class TaskChosenResponse(ChatWorker):
    def __init__(self):
        super().__init__()
        self.base_output = "Based on your input you might be interested in following tasks: \n"

    def work(self, chosen_tasks):
        """
        Stream responses with real-time output
        """
        whole_answer = self.base_output
        for id, task in enumerate(chosen_tasks):
            whole_answer = (
                whole_answer
                + f"{id+1}. "
                + f"**{task.name.replace('_', ' ').capitalize()}**"
                + ": "
                + task.description
                + "\n"
            )
        whole_answer += "Please choose which task suits you best. If you think there is no good task for your needs please specify more details."
        return whole_answer
