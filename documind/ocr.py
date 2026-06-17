from pathlib import Path
from typing import List, Optional

import numpy as np

from documind.document_loader import Document


class OCREngine:
    def __init__(self, languages: List[str] = None):
        self.languages = languages or ["en"]
        self._reader = None

    @property
    def reader(self):
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(self.languages, gpu=False)
        return self._reader

    def ocr_image(self, image: np.ndarray) -> str:
        results = self.reader.readtext(image)
        return "\n".join([text for _, text, _ in results])

    def ocr_pdf(self, pdf_path: str) -> List[Document]:
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pdfplumber is required for PDF OCR")

        docs = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                img = page.to_image(resolution=300)
                img_array = np.array(img.original)
                text = self.ocr_image(img_array)
                if text.strip():
                    docs.append(Document(
                        content=text.strip(),
                        metadata={
                            "source": pdf_path,
                            "page": i + 1,
                            "type": "pdf_ocr",
                        },
                    ))
        if not docs:
            docs.append(Document(
                content="",
                metadata={"source": pdf_path, "page": 0, "type": "pdf_ocr"},
            ))
        return docs

    def ocr_bytes(self, filename: str, data: bytes) -> List[Document]:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            return self.ocr_pdf(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
