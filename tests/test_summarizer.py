import pytest

from documind.document_loader import Document
from documind.summarizer import Summarizer


class MockDemoLLM:
    def ask(self, prompt, context=None, json_mode=False):
        return "[Demo] Summary: This is a mock summary of the document content."


class TestSummarizer:
    def test_init(self):
        s = Summarizer()
        assert s.llm is not None

    def test_styles_defined(self):
        assert "short" in Summarizer.STYLES
        assert "bullet" in Summarizer.STYLES
        assert "detailed" in Summarizer.STYLES
        assert "executive" in Summarizer.STYLES

    def test_summarize_empty_docs(self):
        s = Summarizer(llm=MockDemoLLM())
        result = s.summarize([])
        assert "No documents" in result

    def test_summarize_empty_content(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="", metadata={})]
        result = s.summarize(docs)
        assert "empty" in result.lower()

    def test_summarize_bullet_style(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="Some content to summarize.", metadata={})]
        result = s.summarize(docs, style="bullet")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_summarize_short_style(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="More content here.", metadata={})]
        result = s.summarize(docs, style="short")
        assert isinstance(result, str)

    def test_summarize_detailed_style(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="Detailed content test.", metadata={})]
        result = s.summarize(docs, style="detailed")
        assert isinstance(result, str)

    def test_summarize_executive_style(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="Executive content test.", metadata={})]
        result = s.summarize(docs, style="executive")
        assert isinstance(result, str)

    def test_summarize_invalid_style_falls_back(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="Fallback test.", metadata={})]
        result = s.summarize(docs, style="invalid_style")
        assert isinstance(result, str)

    def test_summarize_by_chunks_empty(self):
        s = Summarizer(llm=MockDemoLLM())
        result = s.summarize_by_chunks([])
        assert "No documents" in result

    def test_summarize_by_chunks_single(self):
        s = Summarizer(llm=MockDemoLLM())
        docs = [Document(content="Single chunk content.", metadata={})]
        result = s.summarize_by_chunks(docs)
        assert isinstance(result, str)
