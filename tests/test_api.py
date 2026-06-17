import pytest
from documind.api.routes import (
    health, stats, list_docs, delete_doc, get_pipeline,
    extract, summarize, ExtractRequest, SummarizeRequest,
)
from fastapi import HTTPException


@pytest.fixture
def auth_user():
    return {"id": 1, "username": "testuser", "role": "user"}


class TestAPIDirect:
    def test_health(self):
        result = health()
        assert result["status"] == "healthy"

    def test_stats(self, auth_user):
        result = stats(current_user=auth_user)
        assert "total_chunks" in result

    def test_list_documents(self, auth_user):
        result = list_docs(current_user=auth_user)
        assert "documents" in result

    def test_delete_nonexistent(self, auth_user):
        with pytest.raises(HTTPException) as exc:
            delete_doc("nonexistent.txt", current_user=auth_user)
        assert exc.value.status_code == 404

    def test_extract_empty(self, auth_user):
        req = ExtractRequest()
        result = extract(req, current_user=auth_user)
        assert "data" in result
        assert "count" in result

    def test_extract_with_query(self, auth_user):
        req = ExtractRequest(query="test query", top_k=5)
        result = extract(req, current_user=auth_user)
        assert "data" in result

    def test_extract_with_schema(self, auth_user):
        req = ExtractRequest(fields_schema={"name": "Name", "age": "Age"})
        result = extract(req, current_user=auth_user)
        assert "data" in result

    def test_summarize_empty(self, auth_user):
        req = SummarizeRequest(source="", style="bullet")
        result = summarize(req, current_user=auth_user)
        assert "summary" in result
        assert "style" in result

    def test_summarize_with_style(self, auth_user):
        for style in ["short", "bullet", "detailed", "executive"]:
            req = SummarizeRequest(source="", style=style)
            result = summarize(req, current_user=auth_user)
            assert result["style"] == style
