from documind.retriever import Retriever


class TestRetriever:
    def test_retrieve(self, populated_store):
        retriever = Retriever(populated_store, top_k=2)
        results = retriever.retrieve("programming language")
        assert len(results) <= 2
        assert len(results) > 0

    def test_retrieve_with_context(self, populated_store):
        retriever = Retriever(populated_store, top_k=2)
        context = retriever.retrieve_with_context("programming language")
        assert isinstance(context, str)
        assert len(context) > 0

    def test_retrieve_with_context_empty_query(self, populated_store):
        retriever = Retriever(populated_store)
        context = retriever.retrieve_with_context("")
        assert isinstance(context, str)

    def test_retrieve_top_k_param(self, populated_store):
        retriever = Retriever(populated_store)
        results = retriever.retrieve("test", top_k=1)
        assert len(results) <= 1

    def test_retrieve_source_metadata(self, populated_store):
        retriever = Retriever(populated_store)
        results = retriever.retrieve("fox")
        if results:
            assert "source" in results[0]["metadata"]
