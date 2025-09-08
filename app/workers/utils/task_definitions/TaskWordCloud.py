from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import WordCloudWorker


class WordCloud(BaseTask):
    name: ClassVar[str] = "word_cloud"
    description: ClassVar[
        str
    ] = """
        This task should create a word cloud (plot in which each term is bigger if it appears more times) out of terms from speeches from accross given time range.
    """
    vizualization_worker: ClassVar[Any] = WordCloudWorker

    min_date: Optional[str] = Field(
        default=None, description="""Minimum date in format DAY-MONTH-YEAR."""
    )

    max_date: Optional[str] = Field(
        default=None, description="""Maximum date in format DAY-MONTH-YEAR."""
    )
