from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Book, Author
from app.admin import setup_admin

app = FastAPI(title="Books API")
# Base.metadata.create_all(bind=engine)

setup_admin(app, engine)

class AuthorCreate(BaseModel):
    name: str
    
class BookCreate(BaseModel):
    title: str
    year: int
    summary: str | None = None
    author_id: int | None = None


@app.get("/")
def root():
    return {"message": "HELLO WORLD"}


@app.get("/books")
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail= "Author not found")
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
    for key, value in payload.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None
