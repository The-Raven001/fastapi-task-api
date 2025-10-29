from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

#The database has been created already using:

#alembic init alembic
#alembic revision --autogenerate -m "create tables"
#alembic upgrade head

"""
Alembic Workflow Overview:

1️⃣ Initialize Alembic (once per project)
   $ alembic init alembic
   - Creates alembic/ folder with env.py, alembic.ini, versions/

2️⃣ Make changes to SQLAlchemy models
   - Example: add new column or table in models.py

3️⃣ Generate migration script
   $ alembic revision --autogenerate -m "describe changes"
   - Compares models vs DB
   - Creates a migration file in alembic/versions/

4️⃣ Apply migration to database
   $ alembic upgrade head
   - Updates DB schema to match models

5️⃣ If DB is dropped / new:
   - Recreate database in PostgreSQL
   - Apply all migrations: $ alembic upgrade head

Workflow Diagram:

   [models.py] ---> [alembic revision --autogenerate] ---> [alembic/versions/*.py]
         |                                                    |
         |                                                    v
         |-----------------------------------------> [Database]
"""