from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas

router = APIRouter(prefix="/tasks", tags=["Tasks"])

#Create task
@router.post("/", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#Get tasks, all/individually
@router.get("/", response_model=list[schemas.Task], status_code=201)
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@router.get("/{id}", response_model=schemas.TaskBase)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#Update task

@router.put("/{id}", response_model=schemas.Task)
def update_item(id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description= updated_task.description
    task.completed= updated_task.completed

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{id}", response_model=schemas.Task)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
