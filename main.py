from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI(title="Git Exercise Todo API")
todo_list = []
current_id = 1
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False
    
class TodoCreate(BaseModel):
    title: str
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy","version":"1.0.0"}

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todo_list

@app.post("/todos", response_model=Todo)
def create_todo(todo_in: TodoCreate):
    global current_id
    new_todo = Todo(
        id = current_id,
        title = todo_in.title,
        completed = todo_in.completed
    )
    todo_list.append(new_todo)
    current_id += 1
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_in: TodoCreate):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.title = todo_in.title
            todo.completed = todo_in.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index,todo in enemuerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)
            return {"message": f"Todo with id {todo_id} has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
