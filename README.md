# 🧠 DocuMind — Document Intelligence with RAG + OCR + Export

**DocuMind** is a professional Document Intelligence platform built on RAG (Retrieval-Augmented Generation). Upload documents, ask questions, extract structured data, and export to Excel. Powered by vector embeddings, semantic search, LLMs, and OCR.

## ✨ Features

- **📄 Multi-format Upload** — PDF, DOCX, TXT, MD with smart chunking
- **🔍 OCR for Scanned PDFs** — Auto-detect scanned documents, extract text via EasyOCR
- **💬 Semantic Search & Q&A** — Sentence embeddings + ChromaDB + LLM-powered answers
- **📝 Summarization** — 4 styles: short, bullet points, detailed, executive
- **🤖 Structured Data Extraction** — Auto-detect or custom schema → JSON
- **📊 Export to Excel** — Formatted .xlsx with headers, filters, and styling
- **⚡ FastAPI Backend** — 9 REST endpoints for integration
- **🎨 Streamlit UI** — 5-page dashboard (Upload, Chat, Summarize, Extract, Knowledge Base)
- **🐳 Docker Ready** — Multi-service deployment (API + UI)

## 🏗️ Architecture

```
DocuMind/
├── documind/                    # Core engine
│   ├── document_loader.py       # PDF/DOCX/TXT/MD parser + OCR auto-detect
│   ├── chunker.py               # Smart text splitting
│   ├── embeddings.py            # Vector embeddings (local)
│   ├── vector_store.py          # ChromaDB vector database
│   ├── retriever.py             # Semantic search engine
│   ├── llm.py                   # LLM adapter (OpenAI/Ollama/Demo)
│   ├── ocr.py                   # EasyOCR for scanned PDFs
│   ├── extractor.py             # Structured data extraction → JSON
│   ├── summarizer.py            # Document summarization (4 styles)
│   ├── exporter.py              # Excel export with formatting
│   ├── qa_pipeline.py           # Full RAG pipeline + extractions
│   └── api/                     # FastAPI backend
├── pages/                       # Streamlit pages
│   ├── 01_Upload_Docs.py        # Document upload interface (with OCR toggle)
│   ├── 02_Chat_QA.py            # Q&A chat interface
│   ├── 03_Knowledge_Base.py     # Manage indexed documents
│   ├── 04_Extract_Export.py     # Structured extraction & Excel export
│   └── 05_Summarize.py          # Document summarization
├── tests/                       # 53+ tests
├── main.py                      # Streamlit entry point
├── Dockerfile + docker-compose.yml
└── requirements.txt
```

## 🚀 Quick Start

### Local

```bash
pip install -r requirements.txt

# Run Streamlit UI
streamlit run main.py

# Or run API server
python -m documind.api.server
```

### Docker

```bash
docker compose up --build
```

- **Streamlit UI**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 Usage

1. **Upload Documents** → Go to Upload Docs page, select PDF/DOCX/TXT/MD files
2. **Ask Questions** → Go to Chat Q&A, type your question
3. **Manage** → View/delete indexed documents in Knowledge Base

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `demo` | `openai`, `ollama`, or `demo` |
| `OPENAI_API_KEY` | — | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.2` | Ollama model name |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Local embedding model |

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | System statistics |
| GET | `/api/documents` | List indexed documents |
| POST | `/api/upload` | Upload a document (with `?force_ocr=true`) |
| POST | `/api/query` | Ask a question |
| POST | `/api/extract` | Extract structured data |
| POST | `/api/summarize` | Summarize documents |
| POST | `/api/export` | Export data to Excel |
| DELETE | `/api/documents/{source}` | Delete a document |

## 🧪 Tests

```bash
pytest tests/ -v
```

Tests covering all modules: document loading, chunking, embeddings, vector store, retrieval, LLM, QA pipeline, extraction, summarization, export, and API.

## 📊 Tech Stack

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (persistent, file-based)
- **OCR**: EasyOCR
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **LLM**: OpenAI / Ollama / Demo mode
- **Export**: openpyxl (formatted Excel)
- **Container**: Docker + Docker Compose (multi-service)

## 📝 License

MIT
