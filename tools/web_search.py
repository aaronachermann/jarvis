import requests
from langchain.tools import tool

@tool
def web_search(query: str) -> str:
    """Return a short web search summary for the given query using DuckDuckGo."""
    try:
        resp = requests.get(
            "https://duckduckgo.com/api",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("Abstract") or data.get("Heading")
        if not answer:
            return "Nessun risultato trovato."
        return answer
    except Exception as e:
        return f"Errore nella ricerca web: {e}"
