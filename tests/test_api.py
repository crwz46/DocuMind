import pytest
from documind.api.routes import (
    health, stats, list_docs, delete_doc, get_pipeline,
    extract, summarize, ExtractRequest, SummarizeRequest,
)
from fastapi import HTTPException


class TestAPIDirect:
    def test_health(self):
        result = health()
        assert result["status"] == "healthy"

    def test_stats(self):
        result = stats(get_pipeline())
        assert "total_chunks" in result

    def test_list_documents(self):
        result = list_docs(get_pipeline())
        assert "documents" in result

    def test_delete_nonexistent(self):
        with pytest.raises(HTTPException) as exc:
            delete_doc("nonexistent.txt", get_pipeline())
        assert exc.value.status_code == 404

    def test_extract_empty(self):
        req = ExtractRequest()
        result = extract(req, get_pipeline())
        assert "data" in result
        assert "count" in result

    def test_extract_with_query(self):
        req = ExtractRequest(query="test query", top_k=5)
        result = extract(req, get_pipeline())
        assert "data" in result

    def test_extract_with_schema(self):
        req = ExtractRequest(fields_schema={"name": "Name", "age": "Age"})
        result = extract(req, get_pipeline())
        assert "data" in result

    def test_summarize_empty(self):
        req = SummarizeRequest(source="", style="bullet")
        result = summarize(req, get_pipeline())
        assert "summary" in result
        assert "style" in result

    def test_summarize_with_style(self):
        for style in ["short", "bullet", "detailed", "executive"]:
            req = SummarizeRequest(source="", style=style)
            result = summarize(req, get_pipeline())
            assert result["style"] == style
