"""Tools for home automation plugin."""
from langchain.tools import tool
from plugins.home_automation import home_automation

@tool
def turn_on_light(room: str) -> str:
    """Accendi la luce in una stanza."""
    return home_automation.turn_on_light(room)

@tool
def turn_off_light(room: str) -> str:
    """Spegni la luce in una stanza."""
    return home_automation.turn_off_light(room)

