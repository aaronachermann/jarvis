"""Tools for the context engine."""
from langchain.tools import tool
from plugins.context import context_engine

@tool
def current_context(_: str = "") -> str:
    """Return basic context such as current time."""
    return context_engine.get_context()
