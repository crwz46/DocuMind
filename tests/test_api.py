import pytest
from documind.api.routes import health, stats, list_docs, delete_doc, get_pipeline
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
