from documind.config import Config
from documind.document_loader import DocumentLoader
from documind.chunker import TextChunker
from documind.embeddings import EmbeddingEngine
from documind.vector_store import VectorStore
from documind.retriever import Retriever
from documind.llm import LLMEngine
from documind.qa_pipeline import QAPipeline
from documind.ocr import OCREngine
from documind.extractor import Extractor
from documind.summarizer import Summarizer
from documind.exporter import ExcelExporter
from documind.auth import register_user, login_user, decode_jwt
from documind.database import UserDB, ConversationDB, init_db

__version__ = "3.0.0"
__all__ = [
    "Config", "DocumentLoader", "TextChunker", "EmbeddingEngine",
    "VectorStore", "Retriever", "LLMEngine", "QAPipeline",
    "OCREngine", "Extractor", "Summarizer", "ExcelExporter",
    "register_user", "login_user", "decode_jwt",
    "UserDB", "ConversationDB", "init_db",
]
