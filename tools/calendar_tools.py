"""Calendar tools using the calendar plugin."""
from langchain.tools import tool
from plugins.calendar import calendar

@tool
def add_event(details: str) -> str:
    """Add an event. Provide details as 'YYYY-MM-DD HH:MM description'."""
    try:
        parts = details.split(maxsplit=2)
        if len(parts) < 3:
            return "Formato non valido."
        date = f"{parts[0]} {parts[1]}"
        description = parts[2]
        calendar.add_event(description, date)
        return "Evento aggiunto al calendario."
    except Exception as e:
        return f"Errore nell'aggiunta dell'evento: {e}"

@tool
def list_events(_: str = "") -> str:
    """List saved events."""
    return calendar.list_events()
