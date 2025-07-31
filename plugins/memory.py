"""Simple conversation memory plugin."""
from pathlib import Path
from typing import List
from . import register, Plugin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Memory(Plugin):
    def __init__(self, path: str = "memory.log"):
        self.path = Path(path)
        self.path.touch(exist_ok=True)

    def setup(self) -> None:
        # nothing to set up currently
        pass

    def store(self, user: str, assistant: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"U: {user}\nA: {assistant}\n")

    def search(self, query: str) -> str:
        try:
            with self.path.open(encoding="utf-8") as f:
                lines = [line.strip() for line in f if query.lower() in line.lower()]
            return "\n".join(lines) if lines else "Nessun risultato."
        except Exception as e:
            return f"Errore nel cercare nei ricordi: {e}"

    def semantic_search(self, query: str) -> str:
        """Search conversation history using simple TF-IDF embeddings."""
        try:
            with self.path.open(encoding="utf-8") as f:
                entries = [line.strip() for line in f if line.strip()]
            if not entries:
                return "Nessun ricordo."  
            vectorizer = TfidfVectorizer().fit(entries + [query])
            vectors = vectorizer.transform(entries + [query])
            sims = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
            if sims.size == 0 or sims.max() == 0:
                return "Nessun risultato rilevante."
            best = entries[sims.argmax()]
            return best
        except Exception as e:
            return f"Errore nella ricerca semantica: {e}"

memory = Memory()
register(memory)

