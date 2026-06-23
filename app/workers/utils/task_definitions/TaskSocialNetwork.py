from workers.utils.task_definitions.TaskBase import BaseTask
from typing import ClassVar, Optional, List
from pydantic import Field
from typing import Any
from workers.worker_classes.results_workers import SocialNetworkWorker


class SocialNetwork(BaseTask):

    name: ClassVar[str] = "social_network"
    description: ClassVar[
        str
    ] = """
        This task should create a social network graph of relations between subjects mentioned in speeches from accross given time range."""
    vizualization_worker: ClassVar[Any] = SocialNetworkWorker

    terms: str = Field(
        default=None,
        description="Terms to be main nodes in social network. All other nodes will be connected to these main nodes. It should look like this: term1,term2,term3",
    )

    window_size: int = Field(
        default=None,
        description="The maximum distance (in terms of number of tokens) between entities to be considered as connected in the graph.",
    )

    minimum_edge_weight: int = Field(
        default=None,
        description="The minimum weight of an edge to be included in the graph.",
    )