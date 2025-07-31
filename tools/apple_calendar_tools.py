"""Tools for interacting with Apple Calendar."""
from langchain.tools import tool
from plugins.apple_calendar import apple_calendar

@tool
def apple_add_event(details: str) -> str:
    """Aggiungi un evento al calendario Apple. Fornisci 'YYYY-MM-DD HH:MM titolo'."""
    try:
        parts = details.split(maxsplit=2)
        if len(parts) < 3:
            return "Formato non valido."
        date = f"{parts[0]} {parts[1]}"
        title = parts[2]
        return apple_calendar.add_event(title, date)
    except Exception as e:
        return f"Errore: {e}"

@tool
def apple_list_events(_: str = "") -> str:
    """Elenca i prossimi eventi dal calendario Apple."""
    return apple_calendar.list_events()
