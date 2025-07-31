from __future__ import annotations
"""Simple local calendar plugin."""
from datetime import datetime
from pathlib import Path
import json
from . import Plugin, register

class Calendar(Plugin):
    def __init__(self, path: str = "calendar.json") -> None:
        self.path = Path(path)
        self.events: list[dict[str, str]] = []

    def setup(self) -> None:
        if self.path.exists():
            try:
                self.events = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.events = []
        else:
            self.path.touch()
            self.events = []

    def add_event(self, description: str, date_str: str) -> None:
        self.events.append({"description": description, "date": date_str})
        self._save()

    def list_events(self) -> str:
        if not self.events:
            return "Nessun evento salvato."
        events = [f"{e['date']}: {e['description']}" for e in self.events]
        return "\n".join(events)

    def _save(self) -> None:
        try:
            self.path.write_text(json.dumps(self.events, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

calendar = Calendar()
register(calendar)
