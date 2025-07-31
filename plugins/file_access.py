"""Plugin to read files from the local system."""
from pathlib import Path
from . import Plugin, register

class FileAccess(Plugin):
    def setup(self) -> None:
        pass

    def read_file(self, path: str) -> str:
        try:
            text = Path(path).read_text(encoding='utf-8')
            return text[:1000]
        except Exception as e:
            return f"Errore nel leggere il file: {e}"

file_access = FileAccess()
register(file_access)

