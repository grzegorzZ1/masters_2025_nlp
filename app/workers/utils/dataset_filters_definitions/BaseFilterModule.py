from pydantic import BaseModel
from typing import ClassVar


class BaseFilter(BaseModel):

    name: ClassVar[str]
    description: ClassVar[str]