from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional, Literal
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import DocsRelatedFinderWorker


class DocsRelatedFinder(BaseTask):

    name: ClassVar[str] = "docs_related_finder"
    description: ClassVar[
        str
    ] = """
        This task should identify related speeches to the short phrase specified by user.
    """
    vizualization_worker: ClassVar[Any] = DocsRelatedFinderWorker

    short_phrase: Optional[str] = Field(
        default=None,
        description="Phrase selected by user, for which worker should perform this task.",
    )

    search_type: Literal["more_like_this"] = Field(
        default="more_like_this",
        description="Type of search used by ElasticSearch engine to find related documents."
    )

    result_count: int = Field(
        default=100,
        description="Number of results user wants to get from this task."
    )