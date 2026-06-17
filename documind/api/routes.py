from functools import lru_cache

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel

from documind.qa_pipeline import QAPipeline

router = APIRouter(prefix="/api")


@lru_cache(maxsize=1)
def get_pipeline() -> QAPipeline:
    return QAPipeline()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list
    context_used: bool


@router.get("/health")
def health():
    return {"status": "healthy", "service": "DocuMind API"}


@router.post("/upload")
async def upload(file: UploadFile = File(...), pipeline: QAPipeline = Depends(get_pipeline)):
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file")
    try:
        result = pipeline.ingest_bytes(file.filename, data)
        if result["status"] == "error":
            raise HTTPException(400, result["message"])
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest, pipeline: QAPipeline = Depends(get_pipeline)):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    return pipeline.query(req.question, top_k=req.top_k)


@router.get("/documents")
def list_docs(pipeline: QAPipeline = Depends(get_pipeline)):
    return {"documents": pipeline.list_documents()}


@router.delete("/documents/{source:path}")
def delete_doc(source: str, pipeline: QAPipeline = Depends(get_pipeline)):
    if not pipeline.delete_document(source):
        raise HTTPException(404, f"Document source not found: {source}")
    return {"status": "deleted", "source": source}


@router.get("/stats")
def stats(pipeline: QAPipeline = Depends(get_pipeline)):
    return pipeline.stats()
