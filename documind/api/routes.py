from functools import lru_cache
from typing import Dict, List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from documind.qa_pipeline import QAPipeline
from documind.database import ConversationDB
from documind.api.auth_routes import get_current_user

router = APIRouter(prefix="/api")


def get_pipeline(user_id: int) -> QAPipeline:
    return QAPipeline(user_id=user_id)


class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    top_k: int = 5


class ExtractRequest(BaseModel):
    query: str = ""
    fields_schema: Dict[str, str] = None
    top_k: int = 10


class SummarizeRequest(BaseModel):
    source: str = ""
    style: str = "bullet"


class CreateConversationRequest(BaseModel):
    title: str = "New Chat"


class UpdateConversationRequest(BaseModel):
    title: str


@router.get("/health")
def health():
    return {"status": "healthy", "service": "DocuMind API"}


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    force_ocr: bool = False,
    current_user: dict = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(400, "No filename provided")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file")
    pipeline = get_pipeline(current_user["id"])
    try:
        result = pipeline.ingest_bytes(file.filename, data, force_ocr=force_ocr)
        if result["status"] == "error":
            raise HTTPException(400, result["message"])
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/query")
def query(
    req: QueryRequest,
    current_user: dict = Depends(get_current_user),
):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    pipeline = get_pipeline(current_user["id"])
    result = pipeline.query(req.question, top_k=req.top_k)

    conv_db = ConversationDB()
    conv_id = req.conversation_id

    if conv_id:
        conv = conv_db.get(conv_id)
        if not conv or conv["user_id"] != current_user["id"]:
            raise HTTPException(404, "Conversation not found")
        conv_db.add_message(conv_id, "user", req.question)
        conv_db.add_message(conv_id, "assistant", result["answer"], sources=result["sources"])
        first_msg = conv_db.get_messages(conv_id)
        if len(first_msg) <= 2:
            title = req.question[:50] + ("..." if len(req.question) > 50 else "")
            conv_db.update_title(conv_id, title)

    return {
        **result,
        "conversation_id": conv_id,
    }


@router.post("/extract")
def extract(
    req: ExtractRequest,
    current_user: dict = Depends(get_current_user),
):
    pipeline = get_pipeline(current_user["id"])
    if req.query:
        result = pipeline.extract_from_chunks(req.query, top_k=req.top_k, schema=req.fields_schema)
    else:
        result = pipeline.extract(schema=req.fields_schema)
    return {"data": result, "count": len(result)}


@router.post("/summarize")
def summarize(
    req: SummarizeRequest,
    current_user: dict = Depends(get_current_user),
):
    pipeline = get_pipeline(current_user["id"])
    source = req.source if req.source else None
    result = pipeline.summarize(source=source, style=req.style)
    return {"summary": result, "style": req.style}


@router.post("/export")
def export(
    req_data: List[Dict],
    filename: str = Query("extracted_data.xlsx"),
    current_user: dict = Depends(get_current_user),
):
    import tempfile
    import os
    pipeline = get_pipeline(current_user["id"])
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    tmp_path = tmp.name
    tmp.close()
    try:
        pipeline.export_excel(req_data, tmp_path)
        return FileResponse(
            tmp_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename,
        )
    except Exception as e:
        os.unlink(tmp_path)
        raise HTTPException(500, f"Export failed: {e}")


@router.get("/documents")
def list_docs(current_user: dict = Depends(get_current_user)):
    pipeline = get_pipeline(current_user["id"])
    return {"documents": pipeline.list_documents()}


@router.delete("/documents/{source:path}")
def delete_doc(source: str, current_user: dict = Depends(get_current_user)):
    pipeline = get_pipeline(current_user["id"])
    if not pipeline.delete_document(source):
        raise HTTPException(404, f"Document source not found: {source}")
    return {"status": "deleted", "source": source}


@router.get("/stats")
def stats(current_user: dict = Depends(get_current_user)):
    pipeline = get_pipeline(current_user["id"])
    return pipeline.stats()


@router.post("/conversations")
def create_conversation(
    req: CreateConversationRequest,
    current_user: dict = Depends(get_current_user),
):
    conv_db = ConversationDB()
    conv = conv_db.create(current_user["id"], title=req.title)
    return {"conversation": conv}


@router.get("/conversations")
def list_conversations(current_user: dict = Depends(get_current_user)):
    conv_db = ConversationDB()
    convs = conv_db.list_by_user(current_user["id"])
    return {"conversations": convs}


@router.get("/conversations/{conv_id}")
def get_conversation(conv_id: str, current_user: dict = Depends(get_current_user)):
    conv_db = ConversationDB()
    conv = conv_db.get(conv_id)
    if not conv or conv["user_id"] != current_user["id"]:
        raise HTTPException(404, "Conversation not found")
    messages = conv_db.get_messages(conv_id)
    return {"conversation": conv, "messages": messages}


@router.put("/conversations/{conv_id}")
def update_conversation(
    conv_id: str,
    req: UpdateConversationRequest,
    current_user: dict = Depends(get_current_user),
):
    conv_db = ConversationDB()
    conv = conv_db.get(conv_id)
    if not conv or conv["user_id"] != current_user["id"]:
        raise HTTPException(404, "Conversation not found")
    conv_db.update_title(conv_id, req.title)
    return {"status": "updated"}


@router.delete("/conversations/{conv_id}")
def delete_conversation(conv_id: str, current_user: dict = Depends(get_current_user)):
    conv_db = ConversationDB()
    conv = conv_db.get(conv_id)
    if not conv or conv["user_id"] != current_user["id"]:
        raise HTTPException(404, "Conversation not found")
    conv_db.delete(conv_id)
    return {"status": "deleted"}
