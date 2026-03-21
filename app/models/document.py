from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id            = Column(Integer, primary_key=True, index=True)
    filename      = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_path     = Column(String(500), nullable=False)
    content       = Column(Text, nullable=True)
    uploaded_by   = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at   = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("User", foreign_keys=[uploaded_by])