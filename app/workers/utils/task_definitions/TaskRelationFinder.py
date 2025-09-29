from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional, List
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import RelationFinderWorker


class RelationFinder(BaseTask):

    name: ClassVar[str] = "relation_finder"
    description: ClassVar[
        str
    ] = """
        This task should identify all times where two subjects specified by user are mentioned in a relation together during specified time range.
    """
    vizualization_worker: ClassVar[Any] = RelationFinderWorker

    subject1: Optional[str] = Field(
        default=None,
        description="First subject from the relation.",
    )

    subject2: Optional[str] = Field(
        default=None,
        description="Second subject from the relation.",
    )