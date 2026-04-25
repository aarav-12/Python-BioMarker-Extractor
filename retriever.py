"""Simple text retriever without vector embeddings."""

from __future__ import annotations


def retrieve(chunks: list[str], query: str, k: int = 3) -> list[str]:
    if not chunks:
        return []

    query_terms = [term for term in query.lower().split() if term]
    scored: list[tuple[int, str]] = []

    for chunk in chunks:
        lower = chunk.lower()
        score = sum(1 for term in query_terms if term in lower)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:k]]
