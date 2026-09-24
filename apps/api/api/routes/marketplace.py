from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.marketplace import Task, TaskApplication
from schemas.marketplace import TaskCreate, TaskResponse, TaskDetailResponse, TaskApplicationCreate, TaskApplicationResponse
from api.routes.social import get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["marketplace"])

@router.get("", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 20, status: str = "OPEN"):
    tasks = db.query(Task).filter(Task.status == status).order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    return tasks

@router.post("", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_task = Task(**task.model_dump(), creator_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{task_id}/take-up", response_model=TaskApplicationResponse)
def apply_to_task(task_id: int, app: TaskApplicationCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.creator_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot apply to your own task")
        
    existing_app = db.query(TaskApplication).filter(TaskApplication.task_id == task_id, TaskApplication.worker_id == user_id).first()
    if existing_app:
        raise HTTPException(status_code=400, detail="Already applied to this task")
        
    db_app = TaskApplication(**app.model_dump(), task_id=task_id, worker_id=user_id)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

@router.post("/{task_id}/applications/{app_id}/accept", response_model=TaskApplicationResponse)
def accept_application(task_id: int, app_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.creator_id != user_id:
        raise HTTPException(status_code=403, detail="Only the task creator can accept applications")
        
    app = db.query(TaskApplication).filter(TaskApplication.id == app_id, TaskApplication.task_id == task_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    app.status = "ACCEPTED"
    task.status = "ASSIGNED"
    db.commit()
    db.refresh(app)
    return app
