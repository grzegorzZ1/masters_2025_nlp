from pydantic import BaseModel, Field, field_validator
from typing import ClassVar, Optional
import json
from pathlib import Path
from typing import Any
from datetime import datetime


class BaseTask(BaseModel):

    name: ClassVar[str]
    description: ClassVar[str]
    vizualization_worker: ClassVar[Any]

    min_date: Optional[str] = Field(
        default=None, description="""Minimum date in format DAY-MONTH-YEAR."""
    )

    max_date: Optional[str] = Field(
        default=None, description="""Maximum date in format DAY-MONTH-YEAR."""
    )

    @property
    def embedding(self):
        with open(f"{Path(__file__).resolve().parent}/embeddings.json") as f:
            return json.load(f)[self.name]

    @field_validator("min_date", "max_date")
    @classmethod
    def validate_date_format(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Date must be in format DD-MM-YYYY")

        return value
