from documind.document_loader import Document


class TestVectorStore:
    def test_empty_store(self, vector_store):
        assert vector_store.count() == 0

    def test_add_documents(self, vector_store, sample_documents):
        count = vector_store.add_documents(sample_documents)
        assert count == 3
        assert vector_store.count() == 3

    def test_search_returns_results(self, populated_store):
        results = populated_store.search("programming language", top_k=2)
        assert len(results) > 0
        assert "id" in results[0]
        assert "content" in results[0]
        assert "metadata" in results[0]
        assert "distance" in results[0]

    def test_search_relevance(self, populated_store):
        results = populated_store.search("programming language", top_k=3)
        found_python = any("Python" in r["content"] for r in results)
        assert found_python

    def test_list_documents(self, populated_store):
        docs = populated_store.list_documents()
        assert len(docs) >= 3

    def test_delete_document(self, populated_store):
        before = populated_store.count()
        deleted = populated_store.delete_document("doc1.txt")
        assert deleted
        assert populated_store.count() == before - 1

    def test_delete_nonexistent(self, populated_store):
        deleted = populated_store.delete_document("nonexistent.txt")
        assert not deleted

    def test_clear(self, populated_store):
        populated_store.clear()
        assert populated_store.count() == 0
