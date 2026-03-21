from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    username   = Column(String(100), unique=True, nullable=False)
    email      = Column(String(255), unique=True, nullable=False)
    password   = Column(String(255), nullable=False)
    role       = Column(Enum("admin", "user"), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    activity_logs = relationship("ActivityLog", back_populates="user")