"""Simple home automation plugin for controlling smart devices."""
from . import Plugin, register

class HomeAutomation(Plugin):
    def setup(self) -> None:
        pass

    def turn_on_light(self, room: str) -> str:
        return f"Luce accesa in {room}."  # placeholder

    def turn_off_light(self, room: str) -> str:
        return f"Luce spenta in {room}."  # placeholder

home_automation = HomeAutomation()
register(home_automation)

