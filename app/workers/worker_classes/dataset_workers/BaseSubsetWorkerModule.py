from abc import ABC, abstractmethod
import ast
from sqlalchemy import create_engine

class BaseSubsetWorker(ABC):
    def __init__(self):
        self.utils_file_path = "app/database_utils/utils.py"
        DATABASE_URL = f"postgresql+psycopg://admin:admin@localhost:5432/speeches"
        self.engine = create_engine(DATABASE_URL, echo=False, future=True)
    
    @staticmethod
    def _get_classes_from_file(filepath):
        with open(filepath, "r") as file:
            node = ast.parse(file.read())
        return [n.name for n in node.body if isinstance(n, ast.ClassDef)]

    @abstractmethod
    def work(self):
        pass