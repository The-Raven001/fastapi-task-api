from fastapi import FastAPI


#examples:

app = FastAPI()

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
    return {"term": term, "limit": limit}


#To start running this api you have to type in the console: uvicorn main:app --reload