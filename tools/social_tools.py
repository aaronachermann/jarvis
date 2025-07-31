"""Tools for the social manager plugin."""
from langchain.tools import tool
from plugins.social import social_manager

@tool
def check_inbox(_: str = "") -> str:
    """Return the latest emails (from local inbox)."""
    return social_manager.triage()
