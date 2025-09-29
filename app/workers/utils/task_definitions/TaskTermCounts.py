from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional, List
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import TermCountsWorker


class TermCounts(BaseTask):

    name: ClassVar[str] = "term_counts"
    description: ClassVar[
        str
    ] = """
        This task should count how many times each specified term appeared in texts during specified time range.
        It can identify in how many speeches term appeared or how many times it appeared accross all texts.
    """
    vizualization_worker: ClassVar[Any] = TermCountsWorker

    terms: Optional[List[str]] = Field(
        default=None,
        description="List of Terms selected by user, for which worker should perform this task. It can contain a single element or few.",
    )