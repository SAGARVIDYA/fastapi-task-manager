from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas
from ..dependencies import get_current_user


router = APIRouter()


# database connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CREATE TASK
@router.post("/tasks")

def create_task(

        task: schemas.TaskCreate,

        current_user: int = Depends(get_current_user),

        db: Session = Depends(get_db)

):

    new_task = models.Task(

        title=task.title,

        description=task.description,

        completed=False,

        owner_id=current_user

    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task


# GET ALL TASKS
@router.get("/tasks")

def get_tasks(

        current_user: int = Depends(get_current_user),

        db: Session = Depends(get_db)

):

    tasks = db.query(

        models.Task

    ).filter(

        models.Task.owner_id == current_user

    ).all()

    return tasks


# GET TASK BY ID
@router.get("/tasks/{task_id}")

def get_task(

        task_id: int,

        current_user: int = Depends(get_current_user),

        db: Session = Depends(get_db)

):

    task = db.query(

        models.Task

    ).filter(

        models.Task.id == task_id,

        models.Task.owner_id == current_user

    ).first()


    if not task:

        raise HTTPException(

            status_code=404,

            detail="Task not found"

        )


    return task


# UPDATE TASK
@router.put("/tasks/{task_id}")

def update_task(

        task_id: int,

        task_update: schemas.TaskUpdate,

        current_user: int = Depends(get_current_user),

        db: Session = Depends(get_db)

):

    task = db.query(

        models.Task

    ).filter(

        models.Task.id == task_id,

        models.Task.owner_id == current_user

    ).first()


    if not task:

        raise HTTPException(

            status_code=404,

            detail="Task not found"

        )


    if task_update.title is not None:

        task.title = task_update.title


    if task_update.description is not None:

        task.description = task_update.description


    if task_update.completed is not None:

        task.completed = task_update.completed


    db.commit()

    db.refresh(task)

    return task


# DELETE TASK
@router.delete("/tasks/{task_id}")

def delete_task(

        task_id: int,

        current_user: int = Depends(get_current_user),

        db: Session = Depends(get_db)

):

    task = db.query(

        models.Task

    ).filter(

        models.Task.id == task_id,

        models.Task.owner_id == current_user

    ).first()


    if not task:

        raise HTTPException(

            status_code=404,

            detail="Task not found"

        )


    db.delete(task)

    db.commit()


    return {

        "message": "Task deleted successfully"

    }