from typing import Any, Dict, List, Optional

from documind.config import Config
from documind.document_loader import Document, DocumentLoader
from documind.chunker import TextChunker
from documind.embeddings import EmbeddingEngine
from documind.vector_store import VectorStore
from documind.retriever import Retriever
from documind.llm import LLMEngine
from documind.extractor import Extractor
from documind.summarizer import Summarizer
from documind.exporter import ExcelExporter


class QAPipeline:
    def __init__(self, store_path: str = None):
        self.embedding_engine = EmbeddingEngine()
        self.vector_store = VectorStore(path=store_path, embedding_engine=self.embedding_engine)
        self.retriever = Retriever(self.vector_store, top_k=5)
        self.chunker = TextChunker()
        self.llm = LLMEngine()
        self.extractor = Extractor(llm=self.llm)
        self.summarizer = Summarizer(llm=self.llm)
        self.exporter = ExcelExporter()

    def extract(self, source: str = None, schema: Dict[str, str] = None) -> List[Dict[str, Any]]:
        if source:
            docs = DocumentLoader.load(source)
        else:
            all_data = self.vector_store.list_documents()
            if not all_data:
                return []
            source = all_data[0]["source"]
            docs = DocumentLoader.load(source)
        return self.extractor.extract(docs, schema=schema)

    def extract_from_chunks(self, query: str, top_k: int = 10, schema: Dict[str, str] = None) -> List[Dict[str, Any]]:
        results = self.retriever.retrieve(query, top_k=top_k)
        docs = [Document(content=r["content"], metadata=r["metadata"]) for r in results]
        return self.extractor.extract(docs, schema=schema)

    def summarize(self, source: str = None, style: str = "bullet") -> str:
        if source:
            docs = DocumentLoader.load(source)
        else:
            all_data = self.vector_store.list_documents()
            if not all_data:
                return "No documents in knowledge base."
            source = all_data[0]["source"]
            docs = DocumentLoader.load(source)
        return self.summarizer.summarize(docs, style=style)

    def export_excel(self, data: List[Dict[str, Any]], output_path: str) -> str:
        return self.exporter.export(data, output_path)

    def ingest(self, file_path: str, force_ocr: bool = False) -> Dict:
        documents = DocumentLoader.load(file_path)
        if not documents or not any(d.content.strip() for d in documents):
            return {"status": "error", "message": "No extractable content found", "chunks": 0}
        chunks = self.chunker.chunk(documents)
        count = self.vector_store.add_documents(chunks)
        return {
            "status": "success",
            "message": f"Processed {count} chunks from {len(documents)} page(s)",
            "chunks": count,
        }

    def ingest_bytes(self, filename: str, data: bytes, force_ocr: bool = False) -> Dict:
        documents = DocumentLoader.load_bytes(filename, data, force_ocr=force_ocr)
        if not documents or not any(d.content.strip() for d in documents):
            return {"status": "error", "message": "No extractable content found", "chunks": 0}
        chunks = self.chunker.chunk(documents)
        count = self.vector_store.add_documents(chunks)
        return {
            "status": "success",
            "message": f"Processed {count} chunks from {len(documents)} page(s)",
            "chunks": count,
        }

    def query(self, question: str, top_k: int = 5) -> Dict:
        context = self.retriever.retrieve_with_context(question, top_k=top_k)
        results = self.retriever.retrieve(question, top_k=top_k)
        answer = self.llm.ask(question, context=context)
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "content": r["content"][:300],
                    "source": r["metadata"].get("source", "unknown"),
                    "page": r["metadata"].get("page"),
                    "distance": r["distance"],
                }
                for r in results
            ],
            "context_used": bool(context),
        }

    def list_documents(self) -> List[Dict]:
        return self.vector_store.list_documents()

    def delete_document(self, source: str) -> bool:
        return self.vector_store.delete_document(source)

    def stats(self) -> Dict:
        return {
            "total_chunks": self.vector_store.count(),
            "documents": len(self.vector_store.list_documents()),
            "embedding_model": self.embedding_engine.model_name,
            "llm_provider": Config.LLM_PROVIDER,
        }
