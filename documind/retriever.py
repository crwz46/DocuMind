from typing import List

from documind.vector_store import VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore, top_k: int = 5):
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str, top_k: int = None) -> List[dict]:
        k = top_k or self.top_k
        return self.vector_store.search(query, top_k=k)

    def retrieve_with_context(self, query: str, top_k: int = None) -> str:
        results = self.retrieve(query, top_k)
        if not results:
            return ""
        context_parts = []
        for i, r in enumerate(results):
            source = r["metadata"].get("source", "unknown")
            page = r["metadata"].get("page", "")
            page_info = f" [Page {page}]" if page else ""
            context_parts.append(
                f"[{i + 1}] Source: {source}{page_info}\n{r['content']}\n"
            )
        return "\n---\n".join(context_parts)
