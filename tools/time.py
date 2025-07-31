# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime
import pytz

@tool
def get_time(city: str) -> str:
    """Returns the current time in a given city."""
    try:
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
        }
        city_key = city.lower()
        if city_key not in city_timezones:
            return f"Scusa, non conosco il fuso orario per {city}."

        timezone = pytz.timezone(city_timezones[city_key])
        current_time = datetime.now(timezone).strftime("%I:%M %p")
        return f"L'ora attuale a {city.title()} è {current_time}."
    except Exception as e:
        return f"Error: {e}"
