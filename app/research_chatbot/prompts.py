DATASET_RESEARCH_PROMPT = """
Our research dataset is a collection of politcal speeches from russia. 
Our analysis focuses on understanding the themes, rhetoric, and strategies employed in these speeches.
"""

SYSTEM_PROMPT = """You are a helpful research assistant.
Provide concise, informative answers to research-related questions.
""" + "\n" + DATASET_RESEARCH_PROMPT

ASK_MORE_CONTEXT_PROMPT = """
Ask one concise follow-up question that would help clarify the research problem."""

CONVERSATION_ROUTER_PROMPT = """Decide whether the research problem is ready to answer or needs more input.
Return only string in one of these forms:
completed if the research problem is ready to answer, or
completed if user do not provde any more details, but instead asks to provide a research problem based on current context, or
need_more_context if more information is needed to clarify the research problem.
"""