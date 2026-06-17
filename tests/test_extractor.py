import json

import pytest

from documind.document_loader import Document
from documind.extractor import Extractor


class MockDemoLLM:
    provider = "demo"

    def ask(self, prompt, context=None, json_mode=False):
        return json.dumps([
            {"name": "John Doe", "age": 30, "city": "Jakarta"},
            {"name": "Jane Smith", "age": 25, "city": "Bandung"},
        ], indent=2)


class TestExtractor:
    def test_init_with_default_llm(self):
        ext = Extractor()
        assert ext.llm is not None

    def test_init_with_custom_llm(self):
        ext = Extractor(llm=MockDemoLLM())
        assert ext.llm.provider == "demo"

    def test_extract_empty_documents(self):
        ext = Extractor(llm=MockDemoLLM())
        result = ext.extract([])
        assert result == []

    def test_extract_returns_list(self):
        ext = Extractor(llm=MockDemoLLM())
        docs = [Document(content="John Doe is 30 years old. He lives in Jakarta.", metadata={})]
        result = ext.extract(docs)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_extract_from_text(self):
        ext = Extractor(llm=MockDemoLLM())
        result = ext.extract_from_text("John Doe is 30 years old. He lives in Jakarta.")
        assert isinstance(result, list)

    def test_extract_with_schema(self):
        ext = Extractor(llm=MockDemoLLM())
        docs = [Document(content="Product A costs $50. Product B costs $75.", metadata={})]
        schema = {"name": "Product name", "price": "Price in dollars"}
        result = ext.extract(docs, schema=schema)
        assert isinstance(result, list)

    def test_build_auto_prompt(self):
        prompt = Extractor._build_auto_prompt("Test content")
        assert "JSON array" in prompt
        assert "Test content" in prompt

    def test_build_schema_prompt(self):
        schema = {"name": "Full name", "age": "Age in years"}
        prompt = Extractor._build_schema_prompt("Test content", schema)
        assert "name" in prompt
        assert "age" in prompt
        assert "Test content" in prompt

    def test_parse_valid_json(self):
        raw = '[{"name": "John", "age": 30}]'
        result = Extractor._parse_result(raw)
        assert len(result) == 1
        assert result[0]["name"] == "John"

    def test_parse_json_with_code_block(self):
        raw = '```json\n[{"name": "John"}]\n```'
        result = Extractor._parse_result(raw)
        assert len(result) == 1
        assert result[0]["name"] == "John"

    def test_parse_single_object(self):
        raw = '{"name": "John"}'
        result = Extractor._parse_result(raw)
        assert len(result) == 1
        assert result[0]["name"] == "John"

    def test_parse_invalid_json(self):
        raw = "This is not JSON at all"
        result = Extractor._parse_result(raw)
        assert len(result) == 1
        assert "error" in result[0]
