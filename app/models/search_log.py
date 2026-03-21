from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class SearchLog(Base):
    __tablename__ = "search_logs"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    query         = Column(String(500), nullable=False)
    results_count = Column(Integer, default=0)
    searched_at   = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")