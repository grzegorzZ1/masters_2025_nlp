from workers.utils.dataset_filters_definitions import BaseFilter
from typing import ClassVar, Optional
from pydantic import Field

class DateFilter(BaseFilter):
    name: ClassVar[str] = "date"
    description: ClassVar[str] = """
        Filter which defines date range for subset. Used when user wants to analyze data only on given period of time.
        Example: User wants to analyze texts from year 2000. It means filter must take only texts from between 01-01-2000 to 31-12-2000.
    """

    min_date: Optional[str] = Field(
        default=None, description="""Minimum date in format DAY-MONTH-YEAR."""
    )

    max_date: Optional[str] = Field(
        default=None, description="""Maximum date in format DAY-MONTH-YEAR."""
    )