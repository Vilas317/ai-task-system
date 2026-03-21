from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog

def log_activity(db: Session, user_id: int, action: str, detail: str = None):
    log = ActivityLog(user_id=user_id, action=action, detail=detail)
    db.add(log)
    db.commit()