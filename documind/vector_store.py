import uuid
from typing import List, Optional

import chromadb
from chromadb.config import Settings

from documind.config import Config
from documind.document_loader import Document
from documind.embeddings import EmbeddingEngine


class VectorStore:
    def __init__(self, path: str = None, embedding_engine: EmbeddingEngine = None):
        self.path = path or Config.VECTOR_STORE_PATH
        self.embedding_engine = embedding_engine or EmbeddingEngine()
        self._client = chromadb.PersistentClient(
            path=self.path,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def collection(self):
        return self._collection

    def add_documents(self, documents: List[Document]) -> int:
        if not documents:
            return 0
        texts = [d.content for d in documents]
        metadatas = [d.metadata for d in documents]
        ids = [str(uuid.uuid4()) for _ in documents]

        embeddings = self.embedding_engine.embed(texts).tolist()
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        return len(documents)

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        total = self.count()
        if total == 0:
            return []
        query_embedding = self.embedding_engine.embed_single(query).tolist()
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, total),
        )
        output = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                output.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if results.get("distances") else 0,
                })
        return output

    def list_documents(self) -> List[dict]:
        all_data = self._collection.get()
        seen = {}
        for i, meta in enumerate(all_data["metadatas"]):
            src = meta.get("source", "unknown")
            if src not in seen:
                seen[src] = {
                    "id": all_data["ids"][i],
                    "source": src,
                    "type": meta.get("type", "unknown"),
                    "chunks": 0,
                }
            seen[src]["chunks"] += 1
        return list(seen.values())

    def delete_document(self, source: str) -> bool:
        all_data = self._collection.get()
        to_delete = []
        for i, meta in enumerate(all_data["metadatas"]):
            if meta.get("source") == source:
                to_delete.append(all_data["ids"][i])
        if to_delete:
            self._collection.delete(ids=to_delete)
            return True
        return False

    def count(self) -> int:
        return self._collection.count()

    def clear(self):
        self._client.delete_collection("documents")
        self._collection = self._client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )
