"""Basic learning module tracking user interactions."""
from pathlib import Path
import json
from . import Plugin, register

class Learning(Plugin):
    def __init__(self, path: str = "learning.json") -> None:
        self.path = Path(path)
        self.stats: dict[str, int] = {}

    def setup(self) -> None:
        if self.path.exists():
            try:
                self.stats = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.stats = {}
        else:
            self.path.touch()
            self.stats = {}

    def record(self, action: str) -> None:
        self.stats[action] = self.stats.get(action, 0) + 1
        try:
            self.path.write_text(json.dumps(self.stats, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def suggest_shortcuts(self) -> str:
        """Suggest actions that occur frequently."""
        if not self.stats:
            return "Nessun dato per suggerimenti."
        most_common = sorted(self.stats.items(), key=lambda x: x[1], reverse=True)[:3]
        suggestions = [f"{act}: {cnt} volte" for act, cnt in most_common if cnt > 1]
        return "; ".join(suggestions) if suggestions else "Nessun pattern ricorrente."

learning = Learning()
register(learning)

