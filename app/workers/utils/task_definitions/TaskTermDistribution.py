from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional
from pydantic import Field

class TermDistribution(BaseTask):

    name: ClassVar[str] = "term_distribution"
    description: ClassVar[str] = """
        This task should create a plot with distribution of appereance in all texts of specific term given by the user throughtout days, months or years.
    """

    min_date: Optional[str] = Field(
        default=None,
        description="""Minimum date in format DAY-MONTH-YEAR."""
    )

    max_date: Optional[str] = Field(
        default=None,
        description="""Maximum date in format DAY-MONTH-YEAR."""
    )

    term: Optional[str] = Field(
        default=None,
        description="Term selected by user, for which worker should define distribution of its presence in speeches"
    )

    granularity: Optional[str] = Field(
        default=None,
        description="Defines whether on timeline user should see appearance on each day, month, or year."
    )