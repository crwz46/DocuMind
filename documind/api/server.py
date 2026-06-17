import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from documind.api.routes import router

app = FastAPI(
    title="DocuMind API",
    version="1.0.0",
    description="Document Q&A with RAG — Upload documents and ask questions",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def run():
    import uvicorn
    from documind.config import Config
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
