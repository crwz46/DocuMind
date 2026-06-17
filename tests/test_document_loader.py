import tempfile
from pathlib import Path

import pytest

from documind.document_loader import DocumentLoader


class TestDocumentLoader:
    def test_load_txt(self, tmp_path):
        fp = tmp_path / "test.txt"
        fp.write_text("Hello DocuMind!", encoding="utf-8")
        docs = DocumentLoader.load(str(fp))
        assert len(docs) == 1
        assert "Hello DocuMind!" in docs[0].content
        assert docs[0].metadata["type"] == "text"

    def test_load_txt_multiple_lines(self, tmp_path):
        content = "Line 1\nLine 2\n\nLine 4"
        fp = tmp_path / "multi.txt"
        fp.write_text(content, encoding="utf-8")
        docs = DocumentLoader.load(str(fp))
        assert len(docs) == 1
        assert "Line 1" in docs[0].content
        assert "Line 4" in docs[0].content

    def test_load_markdown(self, tmp_path):
        fp = tmp_path / "readme.md"
        fp.write_text("# DocuMind\n\nRAG-powered Q&A.", encoding="utf-8")
        docs = DocumentLoader.load(str(fp))
        assert len(docs) == 1
        assert "DocuMind" in docs[0].content

    def test_load_unsupported_extension(self, tmp_path):
        fp = tmp_path / "data.csv"
        fp.write_text("a,b,c", encoding="utf-8")
        with pytest.raises(ValueError, match="Unsupported file type"):
            DocumentLoader.load(str(fp))

    def test_load_from_bytes(self, sample_txt):
        docs = DocumentLoader.load_bytes("test.txt", sample_txt)
        assert len(docs) == 1
        assert "DocuMind" in docs[0].content

    def test_load_bytes_with_unsupported_ext(self, sample_txt):
        with pytest.raises(ValueError, match="Unsupported file type"):
            DocumentLoader.load_bytes("data.csv", sample_txt)

    def test_supported_extensions(self):
        assert ".pdf" in DocumentLoader.SUPPORTED_EXTENSIONS
        assert ".txt" in DocumentLoader.SUPPORTED_EXTENSIONS
        assert ".docx" in DocumentLoader.SUPPORTED_EXTENSIONS
        assert ".md" in DocumentLoader.SUPPORTED_EXTENSIONS

    def test_load_empty_txt(self, tmp_path):
        fp = tmp_path / "empty.txt"
        fp.write_text("", encoding="utf-8")
        docs = DocumentLoader.load(str(fp))
        assert len(docs) == 1
        assert docs[0].content == ""
