from functools import lru_cache
from typing import Dict, List

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
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


class ExtractRequest(BaseModel):
    query: str = ""
    fields_schema: Dict[str, str] = None
    top_k: int = 10


class SummarizeRequest(BaseModel):
    source: str = ""
    style: str = "bullet"


class ExportRequest(BaseModel):
    data: List[Dict]
    filename: str = "extracted_data.xlsx"


@router.get("/health")
def health():
    return {"status": "healthy", "service": "DocuMind API"}


@router.post("/upload")
async def upload(file: UploadFile = File(...), force_ocr: bool = False, pipeline: QAPipeline = Depends(get_pipeline)):
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file")
    try:
        result = pipeline.ingest_bytes(file.filename, data, force_ocr=force_ocr)
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


@router.post("/extract")
def extract(req: ExtractRequest, pipeline: QAPipeline = Depends(get_pipeline)):
    if req.query:
        result = pipeline.extract_from_chunks(req.query, top_k=req.top_k, schema=req.fields_schema)
    else:
        result = pipeline.extract(schema=req.fields_schema)
    return {"data": result, "count": len(result)}


@router.post("/summarize")
def summarize(req: SummarizeRequest, pipeline: QAPipeline = Depends(get_pipeline)):
    source = req.source if req.source else None
    result = pipeline.summarize(source=source, style=req.style)
    return {"summary": result, "style": req.style}


@router.post("/export")
def export(req: ExportRequest, pipeline: QAPipeline = Depends(get_pipeline)):
    import tempfile
    import os
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp_path = tmp.name
    tmp.close()
    try:
        pipeline.export_excel(req.data, tmp_path)
        return FileResponse(
            tmp_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=req.filename,
        )
    except Exception as e:
        os.unlink(tmp_path)
        raise HTTPException(500, f"Export failed: {e}")


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
