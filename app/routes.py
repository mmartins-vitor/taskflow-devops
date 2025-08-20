from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Task, User
from app.schemas import TaskCreate, TaskRead
from app.auth import get_current_user  # <-- import da dependência

# from app.schemas import TaskRead, TaskCreate
from typing import List

router = APIRouter(tags=["tasks"])
#   router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks", response_model=List[TaskRead])
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.post("/tasks", response_model=TaskRead)
def create_taks(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = db.query(Task).get(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = db.query(Task).get(task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}
