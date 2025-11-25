from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker

class SubsetCreator(BaseSubsetWorker):
    def __init__(self, input_params, base_database, subset_database, subset_max_size=10000):
        super().__init__()
        self.subset_database = subset_database
        self.base_database = base_database

        self.subset_max_size = subset_max_size

        self.date_filter = input_params.get("date", None)
        self.keywords_filter = input_params.get("keywords", None)

        self.formatted_base_index_name = self.base_database.replace(" ", "_")
        self.formatted_index_dataset_name = self.subset_database.replace(" ", "_")

    def work(self):
        try:
            print("Refreshing your index...")
            self.es_client.indices.delete(index=self.formatted_index_dataset_name)
        except:
            print("Creating new index...")

        chosen_queries = []
        if self.date_filter:
            chosen_queries.append(self._get_filter_by_date_query(self.date_filter.min_date, self.date_filter.max_date))
        if self.keywords_filter:
            chosen_queries.append(self._get_filter_by_words_query(self.keywords_filter.terms))

        final_query = {
            "bool": {
                "must": chosen_queries
            }
        }

        response = self.es_client.search(
            index=self.formatted_base_index_name,
            query=final_query,
            size=self.subset_max_size
        )
        subset = response["hits"]["hits"]
        index = 0
        for doc in subset:
            index += 1
            self.es_client.index(
                index=self.formatted_index_dataset_name,
                id=index,
                document=doc["_source"]
            )

        return len(subset)

    def _get_filter_by_words_query(self, words, type_of_filter="and"):
        return {
                    "match": {
                        "text": {
                            "query": " ".join(words),
                            "operator": type_of_filter
                        }
                    }
                }

    def _get_filter_by_date_query(self, start_date, end_date):
        formatted_start_date = "-".join(start_date.split("-")[::-1])
        formatted_end_date = "-".join(end_date.split("-")[::-1])
        return {
                    "range": {
                        "date": {
                            "gte": formatted_start_date,
                            "lte": formatted_end_date
                        }
                    }
                }
