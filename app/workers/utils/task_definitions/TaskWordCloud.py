from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Literal, Optional
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import WordCloudWorker


class WordCloud(BaseTask):
    name: ClassVar[str] = "word_cloud"
    description: ClassVar[
        str
    ] = """
        This task should create a word cloud (plot in which each term is bigger if it appears more times) out of terms from speeches from accross given time range.
        Optionally, user can specify a part of speech filter (noun, verb, or adjective) to show only words of that type.
    """
    vizualization_worker: ClassVar[Any] = WordCloudWorker

    pos_filter: Literal["all", "noun", "verb", "adjective"] = Field(
        default="all",
        description="Part-of-speech filter. When set to 'all', all words are shown. When set to 'noun', 'verb', or 'adjective', only words of that type are shown in the word cloud.",
    )

    focus_term: Optional[str] = Field(
        default=None,
        description="Term to focus on. If provided, only words related to this term will be shown in the word cloud.",
    )
