"""Tools for reading files from the host."""
from langchain.tools import tool
from plugins.file_access import file_access

@tool
def read_file(path: str) -> str:
    """Leggi un file locale (solo in lettura)."""
    return file_access.read_file(path)

