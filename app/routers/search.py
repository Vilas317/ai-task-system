from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.search_log import SearchLog
from app.schemas.schemas import SearchRequest, SearchResult
from app.services.ai_search import search_documents
from app.services.logger import log_activity

router = APIRouter()

@router.post("/", response_model=List[SearchResult])
def semantic_search(payload: SearchRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    raw_results = search_documents(payload.query, top_k=payload.top_k)
    db.add(SearchLog(user_id=current_user.id, query=payload.query, results_count=len(raw_results)))
    db.commit()
    log_activity(db, current_user.id, "search", f"Query: '{payload.query}' → {len(raw_results)} results")
    return [
        SearchResult(
            document_id=m["document_id"],
            filename=m["filename"],
            excerpt=m["chunk_text"][:500],
            score=round(s, 4)
        )
        for m, s in raw_results
    ]