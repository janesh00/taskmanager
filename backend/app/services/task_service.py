from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, PaginatedTasks


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=owner_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session,
    owner_id: int,
    page: int = 1,
    page_size: int = 10,
    completed: Optional[bool] = None,
) -> PaginatedTasks:
    query = db.query(Task).filter(Task.owner_id == owner_id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    total = query.count()
    tasks = query.order_by(Task.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedTasks(total=total, page=page, page_size=page_size, tasks=tasks)


def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


def update_task(db: Session, task_id: int, owner_id: int, task_data: TaskUpdate) -> Task:
    task = get_task_by_id(db, task_id, owner_id)
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, owner_id: int) -> None:
    task = get_task_by_id(db, task_id, owner_id)
    db.delete(task)
    db.commit()
