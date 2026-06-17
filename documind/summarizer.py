from typing import List, Optional

from documind.document_loader import Document
from documind.llm import LLMEngine


class Summarizer:
    STYLES = {
        "short": "Summarize in 2-3 sentences.",
        "bullet": "Summarize as bullet points (max 10 points).",
        "detailed": "Write a detailed summary covering all key points.",
        "executive": "Write an executive summary suitable for business stakeholders.",
    }

    def __init__(self, llm: LLMEngine = None):
        self.llm = llm or LLMEngine()

    def summarize(self, documents: List[Document], style: str = "bullet") -> str:
        if not documents:
            return "No documents to summarize."

        full_text = "\n\n".join(d.content for d in documents if d.content.strip())
        if not full_text.strip():
            return "Document is empty."

        style_instruction = self.STYLES.get(style, self.STYLES["bullet"])
        prompt = (
            f"{style_instruction}\n\n"
            f"Focus on the main topics, key facts, data points, and conclusions. "
            f"Be precise and informative.\n\n"
            f"Document:\n{full_text[:8000]}"
        )
        return self.llm.ask(prompt, context=None)

    def summarize_by_chunks(self, documents: List[Document], style: str = "bullet") -> str:
        if not documents:
            return "No documents to summarize."

        chunks = [d.content for d in documents if d.content.strip()]
        if not chunks:
            return "Document is empty."

        style_instruction = self.STYLES.get(style, self.STYLES["bullet"])
        per_chunk = []
        for chunk in chunks[:10]:
            prompt = f"{style_instruction}\n\nChunk:\n{chunk[:3000]}"
            per_chunk.append(self.llm.ask(prompt, context=None))

        if len(per_chunk) <= 1:
            return per_chunk[0] if per_chunk else ""

        combine_prompt = (
            f"Combine the following partial summaries into one coherent {style} summary:\n\n"
            + "\n\n".join(f"Part {i+1}: {s}" for i, s in enumerate(per_chunk))
        )
        return self.llm.ask(combine_prompt, context=None)
