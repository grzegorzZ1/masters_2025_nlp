from sqlalchemy import create_engine, select, and_, or_
from workers.worker_classes.dataset_workers.BaseSubsetWorkerModule import BaseSubsetWorker
from database_utils.utils import *
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path
import textwrap
import importlib

class SubsetCreator(BaseSubsetWorker):
    def __init__(self, input_params, base_database, subset_database):
        super().__init__()
        self.subset_database = subset_database
        self.base_database = base_database

        self.date_filters = input_params.get("date", None)
        self.keywords_filters = input_params.get("keywords", None)
        self.sentiment_filters = input_params.get("sentiment", None)

        self.formatted_base_dataset_name = self.base_database.capitalize().replace(" ", "")
        self.formatted_subset_dataset_name = self.subset_database.capitalize().replace(" ", "")

        self.dataset_module = importlib.import_module("database_utils.utils")
        self.base_dataset_class = getattr(self.dataset_module, self.formatted_base_dataset_name)

        DATABASE_URL = f"postgresql+psycopg://admin:admin@localhost:5432/speeches"
        self.engine = create_engine(DATABASE_URL, echo=False, future=True)

    def work(self):
        self._add_model_class(
            file_path=self.utils_file_path,
            class_name=self.formatted_subset_dataset_name,
            table_name=self.subset_database
        )
        self.dataset_module = importlib.import_module("database_utils.utils")
        self.subset_dataset_class = getattr(self.dataset_module, self.formatted_subset_dataset_name)
        
        try:
            self.subset_dataset_class.__table__.drop(bind=self.engine)
        except:
            print("Creating new dataset...")
        self.subset_dataset_class.__table__.create(bind=self.engine)
        with Session(self.engine) as s:
            stmt = select(self.base_dataset_class)
            
            if self.date_filters:
                stmt = stmt.where(self.base_dataset_class.doc_date.between(
                        datetime.strptime(self.date_filters["min_date"], "%Y-%m-%d").date(),
                        datetime.strptime(self.date_filters["max_date"], "%Y-%m-%d").date()
                    )
                )
            if self.keywords_filters:
                stmt = stmt.where(or_(*[self.base_dataset_class.words.any(word) for word in self.keywords_filters]))
            
            subset_speeches = s.execute(stmt).scalars().all()
            
            for sp in subset_speeches:
                s.add(
                    self.subset_dataset_class(
                        text=sp.text,
                        doc_date=sp.doc_date,
                        words=sp.words,
                        entity_names=sp.entity_names,
                        entity_ids=sp.entity_ids,
                    )
                )

            s.commit()

            return len(subset_speeches)
        
    def _add_model_class(self, file_path, class_name, table_name):
        if not class_name in self._get_classes_from_file(file_path):
            file = Path(file_path)
            class_def = [f"\n\nclass {class_name}(Base):"]
            class_def.append(f'    __tablename__ = "{table_name}"\n')

            class_code = "\n".join(class_def)

            with file.open("a", encoding="utf-8") as f:
                f.write(textwrap.dedent(class_code))
