from langchain_core.messages import AIMessage

from research_chatbot.prompts import SYSTEM_PROMPT
from research_chatbot.utils import ollama_request
from research_chatbot.states import AnalyzerState

def generate_problem_statement(state: AnalyzerState) -> AnalyzerState:
    conversation = []

    for msg in state["messages"]:
        if msg.type == "human":
            conversation.append(f"user: {msg.content}")

    prompt = f"""{SYSTEM_PROMPT}
Conversation so far:
{chr(10).join(conversation)}

Provide the research problem concisely and directly.
"""
    response = ollama_request(prompt, is_stream=False)

    return {
        "messages": [AIMessage(content=response)],
        "response": response,
        "is_problem_defined": True
    }