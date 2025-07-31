"""Context engine plugin for gathering device and location context."""
from datetime import datetime
from typing import Optional
import requests
import psutil
from . import Plugin, register
from .vision import vision

class ContextEngine(Plugin):
    """Gather information about time, location and device activity."""

    def setup(self) -> None:
        self.location_cache: Optional[str] = None

    def _get_location(self) -> str:
        if self.location_cache:
            return self.location_cache
        try:
            resp = requests.get("https://ipinfo.io/json", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            city = data.get("city", "")
            country = data.get("country", "")
            self.location_cache = f"{city}, {country}" if city else country
        except Exception:
            self.location_cache = ""  # ignore errors
        return self.location_cache or "Localita' sconosciuta"

    def _get_activity(self) -> str:
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
            return f"CPU {cpu}% - RAM {mem}%"
        except Exception:
            return "Attivita' sconosciuta"

    def get_context(self) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        location = self._get_location()
        activity = self._get_activity()
        vision_status = vision.capture()
        return f"Ora: {now}; Posizione: {location}; Attivita': {activity}; Visione: {vision_status}"

context_engine = ContextEngine()
register(context_engine)

