from langchain_core.messages import AIMessage

from research_chatbot.prompts import SYSTEM_PROMPT, ASK_MORE_CONTEXT_PROMPT
from research_chatbot.utils import ollama_request
from research_chatbot.states import AnalyzerState


def ask_more_context(state: AnalyzerState) -> AnalyzerState:
    conversation = []

    for msg in state["messages"]:
        if msg.type == "human":
            conversation.append(f"user: {msg.content}")

    prompt = f"""{SYSTEM_PROMPT}
Conversation so far:
{chr(10).join(conversation)}

{ASK_MORE_CONTEXT_PROMPT}
"""
    response = ollama_request(prompt, is_stream=False)

    return {
        "messages": [AIMessage(content=response)],
        "response": response,
        "is_problem_defined": False
    }