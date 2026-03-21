from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import require_admin
from app.models.task import Task
from app.models.document import Document
from app.models.user import User
from app.models.search_log import SearchLog
from app.schemas.schemas import AnalyticsOut

router = APIRouter()

@router.get("/", response_model=AnalyticsOut)
def get_analytics(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    top_searches = (
        db.query(SearchLog.query, func.count(SearchLog.id).label("count"))
        .group_by(SearchLog.query)
        .order_by(func.count(SearchLog.id).desc())
        .limit(5).all()
    )
    return AnalyticsOut(
        total_tasks=db.query(Task).count(),
        completed_tasks=db.query(Task).filter(Task.status == "completed").count(),
        pending_tasks=db.query(Task).filter(Task.status == "pending").count(),
        total_documents=db.query(Document).count(),
        total_users=db.query(User).count(),
        top_searches=[{"query": q, "count": c} for q, c in top_searches]
    )