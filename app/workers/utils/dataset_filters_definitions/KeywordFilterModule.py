from workers.utils.dataset_filters_definitions import BaseFilter
from typing import ClassVar, Optional, List
from pydantic import Field

class KeywordFilter(BaseFilter):
    name: ClassVar[str] = "keyword"
    description: ClassVar[str] = """Filter which takes only texts in which there is present a keyword (or multiple keywords) specified by user.
        Example: User requestt analysis of texts about Poland and Russia. Filter will take only texts where word poland and word russia are present at least one time each.
    """

    terms: Optional[List[str]] = Field(
        default=None,
        description="List of Terms selected by user, for which worker should perform this task. It can contain a single element or few.",
    )