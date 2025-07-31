from langchain.tools import tool
from datetime import datetime
import pytz

@tool
def get_time(city: str) -> str:
    """Get the current time in a given city."""
    city_timezones = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
        "zurich": "Europe/Zurich",
        "rome": "Europe/Rome",
        "paris": "Europe/Paris",
        "berlin": "Europe/Berlin",
        "milan": "Europe/Rome",
        "los angeles": "America/Los_Angeles",
        "san francisco": "America/Los_Angeles",
        "beijing": "Asia/Shanghai",
        "delhi": "Asia/Kolkata",
    }
    try:
        city_key = city.lower()
        if city_key not in city_timezones:
            return f"Scusa, non conosco il fuso orario per {city}."
        timezone = pytz.timezone(city_timezones[city_key])
        current_time = datetime.now(timezone).strftime("%H:%M")
        return f"A {city.title()} sono le {current_time}."
    except Exception as e:
        return f"Errore nel calcolo dell'ora: {e}"
