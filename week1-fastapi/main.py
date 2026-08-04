from fastapi import FastAPI

app = FastAPI(title="Books API")

@app.get("/")
def read_hello():
    return {"message": "hello world"}