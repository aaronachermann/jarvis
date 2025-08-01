"""Utility to automatically load all tools defined in this package."""
from typing import List
from langchain.tools import BaseTool
import importlib
import pkgutil
from config import ENABLED_TOOLS


def load_tools() -> List[BaseTool]:
    """Discover and return all enabled tools in this package."""
    tool_objects: List[BaseTool] = []
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name.startswith("_"):
            continue
        if not ENABLED_TOOLS.get(module_name, False):
            continue
        module = importlib.import_module(f"{__name__}.{module_name}")
        for obj in module.__dict__.values():
            if isinstance(obj, BaseTool):
                tool_objects.append(obj)
    return tool_objects
