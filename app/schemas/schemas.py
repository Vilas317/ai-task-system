from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    user  = "user"

class TaskStatusEnum(str, Enum):
    pending   = "pending"
    completed = "completed"

# ── Auth ──────────────────────────────────────────
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.user

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# ── Tasks ─────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[int] = None

class TaskUpdate(BaseModel):
    status: TaskStatusEnum

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to: Optional[int]
    created_by: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# ── Documents ─────────────────────────────────────
class DocumentOut(BaseModel):
    id: int
    filename: str
    original_name: str
    uploaded_by: int
    uploaded_at: datetime
    class Config:
        from_attributes = True

# ── Search ────────────────────────────────────────
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    document_id: int
    filename: str
    excerpt: str
    score: float

# ── Analytics ─────────────────────────────────────
class AnalyticsOut(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    total_documents: int
    total_users: int
    top_searches: list