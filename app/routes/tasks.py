from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas
from app.routes.auth import get_current_user

router = APIRouter(
    prefix="/tasks", 
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
    )

#Create task
@router.post("/", 
    response_model=schemas.Task, 
    status_code=201,
    summary="Create a new task",
    description="Creates a task owned by the authenticated user."
    )
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        owner_id=current_user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#Get tasks, all/individually
@router.get("/", 
    response_model=list[schemas.Task], 
    status_code=201,
    summary="Retrieves tasks",
    description="Retrieves all tasks owned by the authenticated user.")
def get_tasks(db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()

@router.get("/{id}", 
    response_model=schemas.TaskBase,
    summary="Individually retrieves a task",
    description="Individually retrieves a task owned by the authenticated user."
)
def get_task(id: int, 
            db: Session = Depends(get_db),
            current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == id,
        models.Task.owner_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#Update task

@router.put("/{id}", 
    response_model=schemas.TaskUpdate,
    summary="Update a task",
    description="Updates the selected tasked owned by the authenticated user.")

def update_item(id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description= updated_task.description
    task.completed= updated_task.completed

    db.commit()
    db.refresh(task)
    return task

#Delete task

@router.delete("/{id}", 
    status_code=204,
    summary="Delete a task",
    description="Delete a task owned by the authenticated user.")
def delete_task(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)):

    task = db.query(models.Task).filter(
        models.Task.id == id, 
        models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

    #if you use 200 the line above will show.