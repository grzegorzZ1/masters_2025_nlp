from research_chatbot.prompts import CONVERSATION_ROUTER_PROMPT, SYSTEM_PROMPT
from research_chatbot.utils import ollama_request
from research_chatbot.states import AnalyzerState


def conversation_router(state: AnalyzerState) -> str:
    conversation = []
    if state["is_problem_defined"]:
        return "completed"
    for msg in state["messages"]:
        if msg.type == "human":
            conversation.append(f"user: {msg.content}")

    prompt = f"""{SYSTEM_PROMPT}

{CONVERSATION_ROUTER_PROMPT}

Conversation so far:
{chr(10).join(conversation)}
"""
    return ollama_request(prompt, is_stream=False).replace('"', '').strip()