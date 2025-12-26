from pydantic import BaseModel, EmailStr, Field
from typing import List

#Tasks

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="Cook for mom")
    description:  str | None = Field(None, max_length=255, example="Make pasta and salad")
    

class TaskCreate(TaskBase):
    completed: bool = False

class Task(TaskBase):
    id: int
    completed: bool 

class TaskUpdate(TaskBase):
    completed: bool | None = None
    
    class Config:
        orm_mode = True

#Users

class UserBase(BaseModel):
    username: str = Field(..., example="user1515")
    email: EmailStr = Field(..., example="useremail@example.com")

class UserCreate(UserBase):
    password: str = Field(..., example="12345")

class User(UserBase):
    id: int
    tasks: List[Task] = Field(default_factory=list)

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="useremail@example.com")
    password: str = Field(..., example="12345")

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnYWNtOTUyMThAZ21haWwuY29tIiwiZXhwIjoxNzY2NzE5NjE1fQ.QtDC5RHSYF5u3QcC_QSHz3fk7n2BBwcZB9J_lEEJQEE")
    token_type: str = Field(..., example="bearer")

