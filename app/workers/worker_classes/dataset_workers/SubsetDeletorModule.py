from database_utils.utils import *
from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path
import importlib
import ast
import astor 

class SubsetDeletor(BaseSubsetWorker):
    def __init__(self, subset_database):
        super().__init__()
        self.subset_database = subset_database
        self.formatted_subset_dataset_name = self.subset_database.capitalize().replace(" ", "")

        self.dataset_module = importlib.import_module("database_utils.utils")
        self.subset_dataset_class = getattr(self.dataset_module, self.formatted_subset_dataset_name)

    def work(self):
        self.subset_dataset_class.__table__.drop(bind=self.engine)
        if self.formatted_subset_dataset_name in self._get_classes_from_file(self.utils_file_path):
            self._remove_class_from_file(self.utils_file_path, self.formatted_subset_dataset_name)

    def _remove_class_from_file(self, filepath, class_name):
        with open(filepath, "r") as f:
            source = f.read()

        tree = ast.parse(source)
        new_body = [node for node in tree.body if not (isinstance(node, ast.ClassDef) and node.name == class_name)]
        tree.body = new_body

        new_source = astor.to_source(tree)

        with open(filepath, "w") as f:
            f.write(new_source)