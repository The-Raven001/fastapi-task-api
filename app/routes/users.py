from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import hash, verify
from app.routes.token import create_access_token
from .auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

#Create user
@router.post("/", 
    response_model=schemas.User, 
    status_code=201,
    summary="Creates a new user",
    description="Creates a new user with privileges of creating and handling their own tasks"
    )
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Get users all / individually
@router.get("/", 
    response_model=list[schemas.User], 
    status_code=201,
    summary="Retrieves data of all users",
    description="Retrieves the the username, email, tasks, and user id of all users.")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}", 
    response_model=schemas.User,
    summary="Individually retrieves all the data of a user",
    description="Retrieves the username, email, and tasks of a given user.")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#Update user
@router.put("/{id}", 
    response_model=schemas.User,
    summary="Update data of a given user",
    description="Update username, email, and/or password of a given user.")
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = hash(updated_user.password)
    user.username = updated_user.username
    user.email = updated_user.email
    user.hashed_password = hashed_password

    db.commit()
    db.refresh(user)
    return user

#Delete user

@router.delete("/{id}", 
    response_model=schemas.User,
    summary="Deletes all the data of a given user",
    description="Deletes username, email, password, and tasks of a given user.")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return{"message": "User has been deleted"}

#Login

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

@router.post("/login", 
    response_model=schemas.Token,
    summary="Authentication route",
    description="Authentication route for every user with an existing account")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_credentials.email)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
def read_profile(current_user = Depends(get_current_user)):
    return {
    "message": "This is protected!", 
    "user": current_user.id,
    "email": current_user.email
    }