from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Dependency for routes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
Provides a database session.

- Opens a new SQLAlchemy session
- Ensures the session is closed after request completion

Yields:
    Session: SQLAlchemy database session
"""