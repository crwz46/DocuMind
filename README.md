# 🧠 DocuMind — Document Intelligence with RAG

**DocuMind** is a professional Retrieval-Augmented Generation (RAG) system that lets you upload documents and ask questions about them. Powered by vector embeddings, semantic search, and LLMs.

## ✨ Features

- **📄 Multi-format Upload** — PDF, DOCX, TXT, MD with smart chunking
- **🔍 Semantic Search** — Sentence embeddings + ChromaDB vector store
- **🤖 LLM-Powered Q&A** — OpenAI, Ollama, or Demo mode (zero config)
- **⚡ FastAPI Backend** — 6 REST endpoints for integration
- **🎨 Streamlit UI** — 3-page dashboard (Upload, Chat, Knowledge Base)
- **🐳 Docker Ready** — One-command deployment

## 🏗️ Architecture

```
DocuMind/
├── documind/                    # Core engine
│   ├── document_loader.py       # PDF/DOCX/TXT/MD parser
│   ├── chunker.py               # Smart text splitting
│   ├── embeddings.py            # Vector embeddings (local)
│   ├── vector_store.py          # ChromaDB vector database
│   ├── retriever.py             # Semantic search engine
│   ├── llm.py                   # LLM adapter (OpenAI/Ollama/Demo)
│   ├── qa_pipeline.py           # Full RAG pipeline
│   └── api/                     # FastAPI backend
├── pages/                       # Streamlit pages
│   ├── 01_Upload_Docs.py        # Document upload interface
│   ├── 02_Chat_QA.py            # Q&A chat interface
│   └── 03_Knowledge_Base.py     # Manage indexed documents
├── tests/                       # 53 tests
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
| POST | `/api/upload` | Upload a document |
| POST | `/api/query` | Ask a question |
| DELETE | `/api/documents/{source}` | Delete a document |

## 🧪 Tests

```bash
pytest tests/ -v
```

53 tests covering all modules: document loading, chunking, embeddings, vector store, retrieval, LLM, QA pipeline, and API.

## 📊 Tech Stack

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (persistent, file-based)
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **LLM**: OpenAI / Ollama / Demo mode
- **Container**: Docker + Docker Compose

## 📝 License

MIT
