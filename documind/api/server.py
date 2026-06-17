import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from documind.api.routes import router
from documind.api.auth_routes import router as auth_router

app = FastAPI(
    title="DocuMind API",
    version="3.0.0",
    description="Multi-User Document Intelligence — Auth, RAG, OCR, Extraction, Export, Chat History",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(router)


def run():
    import uvicorn
    from documind.config import Config
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
