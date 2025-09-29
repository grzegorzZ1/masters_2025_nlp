from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional, List
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import RelatedTermCountsWorker


class RelatedTermCounts(BaseTask):

    name: ClassVar[str] = "related_term_counts"
    description: ClassVar[
        str
    ] = """
        This task should identify related terms to the one specified by user.
        Next it should count how many times each of these terms appeared in texts during specified time range.
    """
    vizualization_worker: ClassVar[Any] = RelatedTermCountsWorker

    term: Optional[str] = Field(
        default=None,
        description="Terms selected by user, for which worker should perform this task.",
    )