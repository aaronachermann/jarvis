"""Research assistant plugin for crawling and summarizing web pages."""
import requests
from bs4 import BeautifulSoup
from . import Plugin, register

class ResearchAssistant(Plugin):
    def setup(self) -> None:
        pass

    def crawl(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            text = ' '.join(p.get_text() for p in soup.find_all('p'))
            return text[:1000]
        except Exception as e:
            return f"Errore nel crawling: {e}"

research_assistant = ResearchAssistant()
register(research_assistant)

