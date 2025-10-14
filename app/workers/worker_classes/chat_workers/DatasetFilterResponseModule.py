from workers.worker_classes.chat_workers.ChatWorkerModule import ChatWorker


class DatasetFilterResponse(ChatWorker):
    def __init__(self):
        super().__init__()
        self.base_output = "Based on your input you might be interested in following tasks: \n"

    def work(self, chosen_filters):
        whole_answer = self.base_output
        for id, dict_element in enumerate(chosen_filters.items()):
            filter = dict_element[1]
            whole_answer = (
                whole_answer
                + f"{id+1}. "
                + f"**{filter.name.replace('_', ' ').capitalize()}**"
                + "\n"
            )
            for name, value in filter:
                whole_answer += f"   * {name}: {value}\n"
        whole_answer += "\nIf you think chosen filters are not enough for your needs please specify more details. Otherwise you can create a new sub-dataset using Create Dataset panel below."
        chunk_size = 16
        for i in range(0, len(whole_answer), chunk_size):
            yield whole_answer[i:i+chunk_size]
