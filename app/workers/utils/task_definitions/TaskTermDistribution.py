from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional, List
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import TermDistributionWorker


class TermDistribution(BaseTask):

    name: ClassVar[str] = "term_distribution"
    description: ClassVar[
        str
    ] = """
        This task should create a plot with distribution of appereance in all texts of specific term given by the user throughtout days, months or years.
    """
    vizualization_worker: ClassVar[Any] = TermDistributionWorker

    terms: Optional[List[str]] = Field(
        default=None,
        description="List of Terms selected by user, for which worker should define distribution of its presence in speeches. It can contain a single element or few.",
    )