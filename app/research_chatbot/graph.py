import json
from typing import Optional

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AnyMessage
from langgraph.graph import StateGraph, START, END

from research_chatbot.states import AnalyzerState
from research_chatbot.nodes import (
    ask_more_context,
    generate_problem_statement,
    conversation_router
)

class ResearchChatbot():
    def __init__(self):
        super().__init__()
        self.compiled_graph = self._compile_graph()

    def _compile_graph(self):
        graph_builder = StateGraph(AnalyzerState)

        graph_builder.add_node("state_problem", generate_problem_statement)
        graph_builder.add_node("ask_more_context", ask_more_context)

        graph_builder.add_conditional_edges(
            START,
            conversation_router,
            {
                "completed": "state_problem",
                "need_more_context": "ask_more_context",
            }
        )
        graph_builder.add_edge("state_problem", END)
        graph_builder.add_edge("ask_more_context", END)

        checkpointer = MemorySaver()
        return graph_builder.compile(checkpointer=checkpointer)

    def work(self, messages: list[AnyMessage], thread_id: Optional[str] = None) -> str:
        if not thread_id:
            raise ValueError("Thread ID must be provided.")
        result = self.compiled_graph.invoke(
            {
                "messages": messages,
                "response": "",
                "is_problem_defined": False,
            },
            config={"configurable": {"thread_id": thread_id}},
        )

        return result["response"]
