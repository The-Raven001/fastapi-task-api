from fastapi import FastAPI
from app.routes import tasks, users
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "This is just the landing page"}


"""
examples:

@app.get("/hello")
def say_hello():
    return {"message": "Hello, world!"}

@app.get("/")
def home():
    return {"message": "This should be your home page in the first place"}

#example of how to past data to the URL and then use it
@app.get("/get-test-user/{user_id}")
def get_test(user_id: int):
    return {"user_id": user_id}

#example of sending queries:
@app.get("/search")
def search(term: str, limit: int = 10):
    return {"term": term, "limit": limit}"""