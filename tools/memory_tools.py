"""Tools for interacting with the memory plugin."""
from langchain.tools import tool
from plugins.memory import memory

@tool
def remember(text: str) -> str:
    """Save a piece of text to memory."""
    memory.store("manual note", text)
    return "Ho memorizzato le tue informazioni."

@tool
def recall(query: str) -> str:
    """Search previous conversations for a query."""
    return memory.search(query)

@tool
def semantic_recall(query: str) -> str:
    """Effettua una ricerca semantica nella memoria."""
    return memory.semantic_search(query)

