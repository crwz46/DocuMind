import numpy as np

from documind.embeddings import EmbeddingEngine


class TestEmbeddingEngine:
    def test_embed_texts(self):
        engine = EmbeddingEngine()
        texts = ["Hello world", "RAG pipeline test"]
        result = engine.embed(texts)
        assert isinstance(result, np.ndarray)
        assert result.shape[0] == 2

    def test_embed_single(self):
        engine = EmbeddingEngine()
        result = engine.embed_single("DocuMind test")
        assert isinstance(result, np.ndarray)
        assert result.ndim == 1

    def test_embed_empty_list(self):
        engine = EmbeddingEngine()
        result = engine.embed([])
        assert isinstance(result, np.ndarray)
        assert result.size == 0

    def test_dimension(self):
        engine = EmbeddingEngine()
        assert engine.dimension > 0

    def test_consistency(self):
        engine = EmbeddingEngine()
        text = "DocuMind is a RAG engine"
        v1 = engine.embed_single(text)
        v2 = engine.embed_single(text)
        assert np.allclose(v1, v2)
