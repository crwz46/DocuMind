# 🧠 DocuMind — Multi-User Document Intelligence Platform

**DocuMind** is a professional **multi-user** Document Intelligence platform built on RAG (Retrieval-Augmented Generation). Upload documents, ask questions with **source citations**, chat with **conversation memory**, extract structured data, export to Excel, and more. Each user has an isolated knowledge base.

## ✨ Features

- **🔐 Authentication** — Register/Login with JWT, role-based access
- **👥 Multi-User Workspace** — Each user has their own isolated vector store
- **📄 Multi-format Upload** — PDF, DOCX, TXT, MD with smart chunking
- **🔍 OCR for Scanned PDFs** — Auto-detect scanned documents via EasyOCR
- **💬 Chat Q&A with Citations** — RAG-powered answers with source + page references
- **🕒 Chat History** — Persistent conversations with memory (SQLite)
- **📝 Summarization** — 4 styles: short, bullet points, detailed, executive
- **🤖 Structured Data Extraction** — Auto-detect or custom schema → JSON
- **📊 Export to Excel** — Formatted .xlsx with headers, filters, and styling
- **⚡ FastAPI Backend** — 15+ REST endpoints with JWT auth
- **🎨 Streamlit UI** — 6-page dashboard with login
- **🐳 Docker Ready** — Multi-service deployment (API + UI)

## 🏗️ Architecture

```
DocuMind/
├── documind/                    # Core engine
│   ├── auth.py                  # JWT auth, password hashing
│   ├── database.py              # SQLite: users, conversations, messages
│   ├── document_loader.py       # PDF/DOCX/TXT/MD parser + OCR auto-detect
│   ├── chunker.py               # Smart text splitting
│   ├── embeddings.py            # Vector embeddings (local)
│   ├── vector_store.py          # ChromaDB vector database (per-user)
│   ├── retriever.py             # Semantic search engine
│   ├── llm.py                   # LLM adapter (OpenAI/Ollama/Demo)
│   ├── ocr.py                   # EasyOCR for scanned PDFs
│   ├── extractor.py             # Structured data extraction → JSON
│   ├── summarizer.py            # Document summarization (4 styles)
│   ├── exporter.py              # Excel export with formatting
│   ├── qa_pipeline.py           # Full RAG pipeline + extractions
│   └── api/                     # FastAPI backend
├── pages/                       # Streamlit pages
│   ├── 01_Home.py               # Dashboard with user info
│   ├── 02_Upload_Docs.py        # Document upload (with OCR toggle)
│   ├── 03_Chat_QA.py            # Chat with citations + conversation history
│   ├── 04_Knowledge_Base.py     # Manage indexed documents
│   ├── 05_Extract_Export.py     # Structured extraction & Excel export
│   └── 06_Summarize.py          # Document summarization
├── tests/                       # 108+ tests
├── main.py                      # Login/Register page
├── Dockerfile + docker-compose.yml
└── requirements.txt
```

## 🚀 Quick Start

### Local

```bash
pip install -r requirements.txt

# Run Streamlit UI (login page)
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

1. **Register/Login** → Create an account or login
2. **Upload Documents** → Go to Upload Docs, select PDF/DOCX/TXT/MD files (OCR auto-detected)
3. **Ask Questions** → Go to Chat Q&A, type your question — answers include **source citations**
4. **Chat History** → Conversations are saved automatically, resume anytime
5. **Summarize** → Generate summaries in 4 styles
6. **Extract & Export** → Extract structured data to JSON or Excel

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

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | Login, returns JWT | ❌ |
| GET | `/api/auth/me` | Get current user | ✅ |
| GET | `/api/health` | Health check | ❌ |
| GET | `/api/stats` | System statistics | ✅ |
| GET | `/api/documents` | List indexed documents | ✅ |
| POST | `/api/upload` | Upload a document | ✅ |
| POST | `/api/query` | Ask a question (with `conversation_id`) | ✅ |
| POST | `/api/extract` | Extract structured data | ✅ |
| POST | `/api/summarize` | Summarize documents | ✅ |
| POST | `/api/export` | Export data to Excel | ✅ |
| DELETE | `/api/documents/{source}` | Delete a document | ✅ |
| POST | `/api/conversations` | Create conversation | ✅ |
| GET | `/api/conversations` | List conversations | ✅ |
| GET | `/api/conversations/{id}` | Get conversation + messages | ✅ |
| PUT | `/api/conversations/{id}` | Update conversation title | ✅ |
| DELETE | `/api/conversations/{id}` | Delete conversation | ✅ |

## 🧪 Tests

```bash
pytest tests/ -v
```

108+ tests covering all modules: auth, database, document loading, chunking, embeddings, vector store, retrieval, LLM, OCR, QA pipeline, extraction, summarization, export, and API.

## 📊 Tech Stack

- **Auth**: JWT + bcrypt
- **Database**: SQLite (users, conversations, messages)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (persistent, per-user isolation)
- **OCR**: EasyOCR
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit
- **LLM**: OpenAI / Ollama / Demo mode
- **Export**: openpyxl (formatted Excel)
- **Container**: Docker + Docker Compose (multi-service)

## ☁️ Cloud Deployment

### Deploy to Hugging Face Spaces (Free)

```yaml
# .huggingface.yml
sdk: docker
```

1. Fork this repo
2. Go to [huggingface.co/spaces](https://huggingface.co/spaces) → Create new Space
3. Import your forked repo
4. Set Docker SDK
5. Done! Your Space will be live at `https://username-documind.hf.space`

### Deploy to Railway / Render

```bash
# Railway
railway login
railway init
railway up

# Render: Connect GitHub repo → Set start command:
# docker compose up
```

### Live Demo

> 🔗 **[Try DocuMind Live](https://documind-demo.onrender.com)** — Login with demo/demo

---

## 📝 License

MIT
