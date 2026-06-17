import re
from typing import List

from documind.config import Config
from documind.document_loader import Document


class TextChunker:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP

    def chunk(self, documents: List[Document]) -> List[Document]:
        chunked = []
        for doc in documents:
            if not doc.content.strip():
                continue
            chunks = self._split_text(doc.content)
            for i, chunk_text in enumerate(chunks):
                meta = dict(doc.metadata)
                meta["chunk"] = i
                meta["chunk_total"] = len(chunks)
                chunked.append(Document(content=chunk_text, metadata=meta))
        return chunked

    def _split_text(self, text: str) -> List[str]:
        paragraphs = re.split(r"\n\s*\n", text)
        chunks = []
        current = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current) + len(para) + 1 <= self.chunk_size:
                current = (current + "\n\n" + para).strip() if current else para
            else:
                if current:
                    chunks.append(current)
                current = para

                if len(para) > self.chunk_size:
                    sub_chunks = self._split_large(para)
                    chunks.extend(sub_chunks[:-1])
                    current = sub_chunks[-1]

        if current:
            chunks.append(current)
        return self._apply_overlap(chunks)

    def _split_large(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current = ""
        for sent in sentences:
            if not sent.strip():
                continue
            if len(current) + len(sent) + 1 <= self.chunk_size:
                current = (current + " " + sent).strip() if current else sent
            else:
                if current:
                    chunks.append(current)
                current = sent
                while len(current) > self.chunk_size:
                    chunks.append(current[:self.chunk_size])
                    current = current[self.chunk_size:]
        if current:
            chunks.append(current)
        return chunks

    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        if len(chunks) <= 1 or self.chunk_overlap <= 0:
            return chunks
        result = [chunks[0]]
        for i in range(1, len(chunks)):
            prev = chunks[i - 1]
            overlap = prev[-self.chunk_overlap:] if len(prev) > self.chunk_overlap else prev
            result.append(overlap + chunks[i])
        return result
