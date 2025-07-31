"""Tools for the learning module."""
from langchain.tools import tool
from plugins.learning import learning

@tool
def record_action(action: str) -> str:
    """Record an action in the learning module."""
    learning.record(action)
    return "Azione registrata."
