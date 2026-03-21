from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.task import Task
from app.models.user import User
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskOut
from app.services.logger import log_activity

router = APIRouter()

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    if payload.assigned_to:
        if not db.query(User).filter(User.id == payload.assigned_to).first():
            raise HTTPException(status_code=404, detail="Assigned user not found")
    task = Task(
        title=payload.title,
        description=payload.description,
        assigned_to=payload.assigned_to,
        created_by=current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=List[TaskOut])
def list_tasks(
    status: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task)
    if current_user.role != "admin":
        query = query.filter(Task.assigned_to == current_user.id)
    if status:
        query = query.filter(Task.status == status)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    return query.order_by(Task.created_at.desc()).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != "admin" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return task

@router.patch("/{task_id}", response_model=TaskOut)
def update_task_status(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != "admin" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    old_status = task.status
    task.status = payload.status
    db.commit()
    db.refresh(task)
    log_activity(db, current_user.id, "task_update", f"Task {task_id}: '{old_status}' → '{payload.status}'")
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()