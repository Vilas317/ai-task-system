import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.document import Document
from app.models.user import User
from app.schemas.schemas import DocumentOut
from app.services.ai_search import add_document_to_index, remove_document_from_index
from app.services.logger import log_activity

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text(file_path: str, filename: str) -> str:
    if filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if filename.endswith(".pdf"):
        try:
            import fitz
            doc  = fitz.open(file_path)
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except ImportError:
            return ""
    return ""

@router.post("/upload", response_model=DocumentOut, status_code=201)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".txt", ".pdf"]:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are allowed")
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = extract_text(file_path, file.filename)
    document = Document(
        filename=unique_filename,
        original_name=file.filename,
        file_path=file_path,
        content=text[:5000],
        uploaded_by=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    if text:
        add_document_to_index(document.id, file.filename, text)
    log_activity(db, current_user.id, "document_upload", f"Uploaded '{file.filename}'")
    return document

@router.get("/", response_model=List[DocumentOut])
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()

@router.get("/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{doc_id}", status_code=204)
def delete_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    remove_document_from_index(doc_id)
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    db.delete(doc)
    db.commit()