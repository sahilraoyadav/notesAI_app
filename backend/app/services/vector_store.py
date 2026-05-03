from typing import Iterable


class InMemoryVectorStore:
    def __init__(self):
        self.docs: dict[int, tuple[str, list[float]]] = {}

    def upsert(self, note_id: int, text: str, emb: list[float]) -> None:
        self.docs[note_id] = (text, emb)

    def semantic_search(self, query: str, k: int = 5) -> Iterable[int]:
        scored = []
        for note_id, (text, _emb) in self.docs.items():
            score = sum(1 for tok in query.lower().split() if tok in text.lower())
            scored.append((score, note_id))
        scored.sort(reverse=True)
        return [n for s, n in scored if s > 0][:k]


vector_store = InMemoryVectorStore()
