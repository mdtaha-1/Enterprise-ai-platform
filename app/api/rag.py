import os
import shutil
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.rag.pipeline import ingest_pdf, query_documents

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a PDF document"""
    upload_path = f"./data/{file.filename}"
    os.makedirs("./data", exist_ok=True)

    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_id = file.filename.replace(".pdf", "")
    chunks = ingest_pdf(upload_path, doc_id)

    return {
        "message": f"Document ingested successfully",
        "filename": file.filename,
        "chunks_stored": chunks
    }

@router.post("/query")
async def query_document(request: QueryRequest):
    """Ask a question about uploaded documents"""
    answer = query_documents(request.question)
    return {"answer": answer}