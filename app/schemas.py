from pydantic import BaseModel, EmailStr

class TaskBase(BaseModel):
    title: str
    description:  str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool

class Config:
    orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

"""
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")"""