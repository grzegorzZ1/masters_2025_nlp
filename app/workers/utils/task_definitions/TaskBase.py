from pydantic import BaseModel
from typing import ClassVar
import json
from pathlib import Path
from typing import Any


class BaseTask(BaseModel):

    name: ClassVar[str]
    description: ClassVar[str]
    vizualization_worker: ClassVar[Any]

    @property
    def embedding(self):
        with open(f"{Path(__file__).resolve().parent}/embeddings.json") as f:
            return json.load(f)[self.name]
