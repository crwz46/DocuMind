import numpy as np
import pytest

from documind.ocr import OCREngine


class TestOCREngine:
    def test_init_default_language(self):
        ocr = OCREngine()
        assert ocr.languages == ["en"]

    def test_init_custom_language(self):
        ocr = OCREngine(languages=["en", "id"])
        assert ocr.languages == ["en", "id"]

    def test_reader_lazy_loaded(self):
        ocr = OCREngine()
        assert ocr._reader is None
        _ = ocr.reader
        assert ocr._reader is not None

    def test_ocr_image_empty(self, monkeypatch):
        class MockReader:
            def readtext(self, image):
                return []

        monkeypatch.setattr("easyocr.Reader", lambda *a, **kw: MockReader())
        ocr = OCREngine()
        result = ocr.ocr_image(np.zeros((100, 100, 3), dtype=np.uint8))
        assert result == ""

    def test_ocr_image_with_text(self, monkeypatch):
        class MockReader:
            def readtext(self, image):
                return [
                    ([[0, 0], [10, 0], [10, 5], [0, 5]], "Hello OCR", 0.95),
                    ([[0, 10], [20, 10], [20, 15], [0, 15]], "Test Document", 0.92),
                ]

        monkeypatch.setattr("easyocr.Reader", lambda *a, **kw: MockReader())
        ocr = OCREngine()
        result = ocr.ocr_image(np.zeros((100, 100, 3), dtype=np.uint8))
        assert "Hello OCR" in result
        assert "Test Document" in result

    def test_ocr_pdf_returns_documents(self, monkeypatch, tmp_path):
        pdf_path = tmp_path / "scan.pdf"
        pdf_path.write_bytes(b"%PDF-1.4\nfake pdf content\n%%EOF")

        class MockReader:
            def readtext(self, image):
                return [([[0, 0], [10, 0], [10, 5], [0, 5]], "Scanned Page 1", 0.95)]

        monkeypatch.setattr("easyocr.Reader", lambda *a, **kw: MockReader())

        class MockPage:
            def to_image(self, resolution=300):
                class MockImg:
                    original = np.zeros((100, 100, 3), dtype=np.uint8)
                return MockImg()

        class MockPDF:
            def __init__(self, *a, **kw):
                self.pages = [MockPage()]

            def __enter__(self):
                return self

            def __exit__(self, *a):
                pass

        monkeypatch.setattr("pdfplumber.open", lambda p: MockPDF())

        ocr = OCREngine()
        docs = ocr.ocr_pdf(str(pdf_path))
        assert len(docs) >= 1
        assert docs[0].metadata["type"] == "pdf_ocr"

    def test_ocr_bytes(self, monkeypatch, tmp_path):
        data = b"%PDF-1.4\nfake\n%%EOF"

        class MockReader:
            def readtext(self, image):
                return [([[0, 0], [10, 0], [10, 5], [0, 5]], "OCR from bytes", 0.95)]

        monkeypatch.setattr("easyocr.Reader", lambda *a, **kw: MockReader())

        class MockPage:
            def to_image(self, resolution=300):
                class MockImg:
                    original = np.zeros((100, 100, 3), dtype=np.uint8)
                return MockImg()

        class MockPDF:
            def __init__(self, *a, **kw):
                self.pages = [MockPage()]

            def __enter__(self):
                return self

            def __exit__(self, *a):
                pass

        monkeypatch.setattr("pdfplumber.open", lambda p: MockPDF())

        ocr = OCREngine()
        docs = ocr.ocr_bytes("scan.pdf", data)
        assert len(docs) >= 1
