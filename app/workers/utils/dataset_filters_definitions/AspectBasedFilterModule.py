from workers.utils.dataset_filters_definitions import BaseFilter
from typing import ClassVar, Optional, Dict
from pydantic import Field

class AspectBasedFilter(BaseFilter):
    name: ClassVar[str] = "aspect_based"
    description: ClassVar[str] = """
        Filter which chooses only texts which there is a mention of each of terms specified by user, but each terms is mentioned with a sentiment chosen by user.
        Example: User requests analysis of text with positive mention about Poland. It means filter will take only texts where Poland is mentioned in positive way.
    """

    terms: Optional[Dict[str, str]] = Field(
        default=None,
        description="""
            Dictionary of Terms selected by user, for which worker should perform this task, where:
            - keys are strings containing term itself
            - values are sentiments related to key terms
        """,
    )