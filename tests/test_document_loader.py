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

    def test_is_scanned_true(self, tmp_path):
        fp = tmp_path / "textless.pdf"
        fp.write_bytes(b"%PDF-1.4\n%%EOF")
        from documind.document_loader import Document
        docs = [Document(content="", metadata={"source": str(fp), "type": "pdf"})]
        assert DocumentLoader._is_scanned(docs)

    def test_is_scanned_false(self, tmp_path):
        from documind.document_loader import Document
        docs = [Document(content="This is a real document with plenty of text content.", metadata={})]
        assert not DocumentLoader._is_scanned(docs)

    def test_force_ocr_flag(self, monkeypatch, tmp_path):
        fp = tmp_path / "scan.pdf"
        fp.write_bytes(b"%PDF-1.4\nfake content\n%%EOF")

        class MockReader:
            def readtext(self, image):
                return [([[0, 0], [10, 0], [10, 5], [0, 5]], "OCR text", 0.95)]

        monkeypatch.setattr("easyocr.Reader", lambda *a, **kw: MockReader())

        class MockImg:
            original = __import__("numpy").zeros((100, 100, 3), dtype="uint8")

        class MockPage:
            def extract_text(self):
                return ""
            def to_image(self, resolution=300):
                return MockImg()

        class MockPDF:
            def __init__(self, *a, **kw):
                self.pages = [MockPage()]
            def __enter__(self):
                return self
            def __exit__(self, *a):
                pass

        monkeypatch.setattr("pdfplumber.open", lambda p: MockPDF())

        docs = DocumentLoader.load(str(fp), force_ocr=True)
        assert any("OCR text" in d.content for d in docs)
