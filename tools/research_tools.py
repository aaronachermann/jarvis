"""Tools for the research assistant plugin."""
from langchain.tools import tool
from plugins.research import research_assistant

@tool
def crawl(url: str) -> str:
    """Crawl a webpage and return a short summary."""
    return research_assistant.crawl(url)

