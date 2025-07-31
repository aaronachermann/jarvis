"""Plugin utilities for Jarvis."""
from typing import Protocol
import importlib
import pkgutil

class Plugin(Protocol):
    def setup(self) -> None:
        """Optional setup called on startup."""


registered_plugins: list[Plugin] = []

def register(plugin: Plugin) -> None:
    registered_plugins.append(plugin)


def _discover() -> None:
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{module_name}")


def setup_plugins() -> None:
    _discover()
    for plugin in registered_plugins:
        try:
            plugin.setup()
        except Exception:
            pass
