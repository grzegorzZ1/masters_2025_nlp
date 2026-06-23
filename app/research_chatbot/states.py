from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from typing import Annotated, TypedDict


class AnalyzerState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    response: str
    is_problem_defined: bool
