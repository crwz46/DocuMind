import tempfile
from pathlib import Path

import pytest

from documind.config import Config
from documind.document_loader import Document
from documind.embeddings import EmbeddingEngine
from documind.vector_store import VectorStore


@pytest.fixture(autouse=True)
def reset_config():
    Config.LLM_PROVIDER = "demo"
    return Config


@pytest.fixture
def sample_pdf():
    content = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>endobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF"
    return content


@pytest.fixture
def sample_txt():
    return b"DocuMind is a RAG-powered document Q&A engine.\nIt uses vector search and LLMs to answer questions."


@pytest.fixture
def sample_doc():
    return Document(
        content="DocuMind is a RAG-powered document Q&A engine. "
                "It uses vector search and LLMs to answer questions based on provided context.",
        metadata={"source": "test.txt", "type": "text"},
    )


@pytest.fixture
def sample_documents():
    return [
        Document(
            content="The quick brown fox jumps over the lazy dog. "
                    "This is a test document for semantic search.",
            metadata={"source": "doc1.txt", "type": "text"},
        ),
        Document(
            content="Python is a programming language. "
                    "It is used for data science, web development, and automation.",
            metadata={"source": "doc2.txt", "type": "text"},
        ),
        Document(
            content="Retrieval Augmented Generation combines retrieval and generation "
                    "for better answers. It uses vector databases.",
            metadata={"source": "doc3.txt", "type": "text"},
        ),
    ]


@pytest.fixture
def vector_store(tmp_path):
    store_path = str(tmp_path / "chroma_test")
    emb = EmbeddingEngine()
    vs = VectorStore(path=store_path, embedding_engine=emb)
    yield vs
    import shutil
    shutil.rmtree(store_path, ignore_errors=True)


@pytest.fixture
def populated_store(vector_store, sample_documents):
    vector_store.add_documents(sample_documents)
    return vector_store
