import tempfile
from pathlib import Path

import pytest

from documind.qa_pipeline import QAPipeline


class TestQAPipeline:
    @pytest.fixture
    def fresh_pipeline(self, tmp_path):
        return QAPipeline(store_path=str(tmp_path / "db"))

    def test_stats_empty(self, fresh_pipeline):
        stats = fresh_pipeline.stats()
        assert stats["total_chunks"] == 0
        assert stats["documents"] == 0

    def test_ingest_txt(self, fresh_pipeline, tmp_path):
        fp = tmp_path / "test.txt"
        fp.write_text("DocuMind is a RAG engine for document Q&A.", encoding="utf-8")
        result = fresh_pipeline.ingest(str(fp))
        assert result["status"] == "success"
        assert result["chunks"] > 0

    def test_ingest_bytes(self, fresh_pipeline, sample_txt):
        result = fresh_pipeline.ingest_bytes("test.txt", sample_txt)
        assert result["status"] == "success"
        assert result["chunks"] > 0

    def test_ingest_empty_bytes(self, fresh_pipeline):
        result = fresh_pipeline.ingest_bytes("empty.txt", b"")
        assert result["status"] == "error"

    def test_query_after_ingest(self, fresh_pipeline, tmp_path):
        fp = tmp_path / "doc.txt"
        fp.write_text(
            "Python is a programming language used for data science, "
            "web development, and machine learning. "
            "It was created by Guido van Rossum.",
            encoding="utf-8",
        )
        fresh_pipeline.ingest(str(fp))
        result = fresh_pipeline.query("What is Python?")
        assert result["question"] == "What is Python?"
        assert len(result["answer"]) > 0
        assert len(result["sources"]) > 0
        assert result["context_used"]

    def test_query_empty_kb(self, tmp_path):
        pipeline = QAPipeline(store_path=str(tmp_path / "empty_test"))
        result = pipeline.query("What is the meaning of life?")
        assert result["question"] == "What is the meaning of life?"
        assert len(result["sources"]) == 0

    def test_list_documents(self, fresh_pipeline, tmp_path):
        fp = tmp_path / "list_test.txt"
        fp.write_text("Test document listing.", encoding="utf-8")
        fresh_pipeline.ingest(str(fp))
        docs = fresh_pipeline.list_documents()
        assert len(docs) >= 1

    def test_delete_document(self, fresh_pipeline, tmp_path):
        fp = tmp_path / "delete_me.txt"
        fp.write_text("Delete this document.", encoding="utf-8")
        fresh_pipeline.ingest(str(fp))
        deleted = fresh_pipeline.delete_document(str(fp))
        assert deleted
        docs = fresh_pipeline.list_documents()
        assert all(d["source"] != str(fp) for d in docs)

    def test_delete_nonexistent(self, fresh_pipeline):
        assert not fresh_pipeline.delete_document("nonexistent.txt")

    def test_stats_after_ingest(self, fresh_pipeline, tmp_path):
        fp = tmp_path / "stats.txt"
        fp.write_text("Stats test document content.", encoding="utf-8")
        fresh_pipeline.ingest(str(fp))
        stats = fresh_pipeline.stats()
        assert stats["total_chunks"] > 0
        assert stats["documents"] > 0
        assert "embedding_model" in stats
        assert "llm_provider" in stats
