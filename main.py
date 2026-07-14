from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI(title="Git Exercise Todo API")
todo_list = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todo_list

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    todo_list.append(todo)
    return todo
