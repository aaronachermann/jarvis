"""Basic social manager plugin."""
from pathlib import Path
from . import Plugin, register

class SocialManager(Plugin):
    def __init__(self, inbox: str = "inbox.txt") -> None:
        self.inbox = Path(inbox)

    def setup(self) -> None:
        self.inbox.touch(exist_ok=True)

    def triage(self) -> str:
        try:
            lines = self.inbox.read_text(encoding="utf-8").strip().splitlines()
            if not lines:
                return "Nessuna email da gestire."
            latest = lines[-5:]
            return "\n".join(latest)
        except Exception as e:
            return f"Errore nella lettura dell'inbox: {e}"

social_manager = SocialManager()
register(social_manager)
