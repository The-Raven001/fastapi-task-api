from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import hash, verify

router = APIRouter(prefix="/users", tags=["Users"])

#Create user
@router.post("/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Get users all / individually
@router.get("/", response_model=list[schemas.User], status_code=201)
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#Update user
@router.put("/{id}", response_model=schemas.User)
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

@router.delete("/{id}", response_model=schemas.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return{"message": "User has been deleted"}