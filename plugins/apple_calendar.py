"""Apple Calendar integration using macOS EventKit."""
from __future__ import annotations
from datetime import datetime, timedelta
from . import Plugin, register

try:
    import objc  # type: ignore
    from Foundation import NSDate
    from EventKit import EKEventStore, EKSpanThisEvent
    MACOS = True
except Exception:
    MACOS = False


class AppleCalendar(Plugin):
    def setup(self) -> None:
        if not MACOS:
            self.store = None
            return
        try:
            self.store = EKEventStore.alloc().init()
            self.store.requestAccessToEntityType_completion_(0, None)
        except Exception:
            self.store = None

    def add_event(self, title: str, date_str: str) -> str:
        """Add an event to Apple Calendar."""
        if not self.store:
            return "Apple Calendar non disponibile."
        try:
            start = datetime.fromisoformat(date_str)
            end = start + timedelta(hours=1)
            event = self.store.eventWithIdentifier_("new")  # placeholder
            event = self.store.eventStore().eventWithIdentifier_("new") if hasattr(self.store, 'eventStore') else self.store.eventWithIdentifier_("new")
            event = event or objc.lookUpClass('EKEvent').eventWithEventStore_(self.store)
            event.setTitle_(title)
            event.setStartDate_(NSDate.dateWithTimeIntervalSince1970_(start.timestamp()))
            event.setEndDate_(NSDate.dateWithTimeIntervalSince1970_(end.timestamp()))
            event.setCalendar_(self.store.defaultCalendarForNewEvents())
            self.store.saveEvent_span_error_(event, EKSpanThisEvent, None)
            return "Evento aggiunto al calendario Apple."
        except Exception as e:
            return f"Errore nell'aggiunta dell'evento: {e}"

    def list_events(self) -> str:
        """List upcoming events from Apple Calendar."""
        if not self.store:
            return "Apple Calendar non disponibile."
        try:
            start = NSDate.date()
            end = NSDate.dateWithTimeIntervalSinceNow_(60 * 60 * 24 * 7)
            predicate = self.store.predicateForEventsWithStartDate_endDate_calendars_(start, end, None)
            events = self.store.eventsMatchingPredicate_(predicate)
            if not events:
                return "Nessun evento in programma."
            lines = []
            for e in events:
                start_ts = e.startDate().timeIntervalSince1970()
                date_str = datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M")
                lines.append(f"{date_str}: {e.title()}")
            return "\n".join(lines)
        except Exception as e:
            return f"Errore nel recupero degli eventi: {e}"

apple_calendar = AppleCalendar()
register(apple_calendar)

