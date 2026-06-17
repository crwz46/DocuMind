import pytest

from documind.chunker import TextChunker
from documind.document_loader import Document


class TestTextChunker:
    def test_single_small_doc(self):
        chunker = TextChunker(chunk_size=500, chunk_overlap=0)
        doc = Document(content="Hello world", metadata={"source": "test.txt"})
        result = chunker.chunk([doc])
        assert len(result) == 1
        assert result[0].content == "Hello world"

    def test_large_doc_splits_into_chunks(self):
        chunker = TextChunker(chunk_size=50, chunk_overlap=0)
        text = " ".join(["word"] * 200)
        doc = Document(content=text, metadata={"source": "test.txt"})
        result = chunker.chunk([doc])
        assert len(result) > 1

    def test_multi_paragraph_chunking(self):
        chunker = TextChunker(chunk_size=200, chunk_overlap=0)
        text = "\n\n".join([f"Paragraph {i} " * 10 for i in range(5)])
        doc = Document(content=text, metadata={"source": "test.txt"})
        result = chunker.chunk([doc])
        assert len(result) >= 2

    def test_chunk_metadata_inherited(self):
        chunker = TextChunker(chunk_size=50, chunk_overlap=0)
        doc = Document(
            content="A B C. " * 30,
            metadata={"source": "doc.txt", "type": "text", "author": "test"},
        )
        result = chunker.chunk([doc])
        for r in result:
            assert r.metadata["source"] == "doc.txt"
            assert r.metadata["author"] == "test"
            assert "chunk" in r.metadata
            assert "chunk_total" in r.metadata

    def test_empty_document_skipped(self):
        chunker = TextChunker(chunk_size=100, chunk_overlap=0)
        doc = Document(content="", metadata={"source": "empty.txt"})
        result = chunker.chunk([doc])
        assert len(result) == 0

    def test_overlap_applied(self):
        chunker = TextChunker(chunk_size=100, chunk_overlap=30)
        text = " ".join(["word"] * 50)
        doc = Document(content=text, metadata={"source": "test.txt"})
        result = chunker.chunk([doc])
        if len(result) > 1:
            assert result[0].content[-30:] in result[1].content

    def test_chunk_index_tracking(self):
        chunker = TextChunker(chunk_size=30, chunk_overlap=5)
        text = " ".join(["word"] * 30)
        doc = Document(content=text, metadata={"source": "test.txt"})
        result = chunker.chunk([doc])
        assert result[0].metadata["chunk"] == 0
        if len(result) > 1:
            assert result[1].metadata["chunk"] == 1
