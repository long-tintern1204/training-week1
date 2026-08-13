from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Author, Book
from app.schemas.book import BookCreate, BookRead, BookUpdate


def to_book_read(book: Book) -> BookRead:
    return BookRead(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        author_name=book.author.name if book.author else None,
        summary=book.summary,
        year=book.year
    )

def _ensure_author_exists(db: Session, author_id: int | None) -> None:
    if author_id is None:
        return
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    
def list_books(db: Session) -> list[BookRead]:
    stmt = select(Book).options(joinedload(Book.author))
    books = db.scalars(stmt).all()
    return [to_book_read(book) for book in books]


def get_book(db: Session, book_id: int) -> BookRead:
    stmt = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
    book = db.scalar(stmt)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return to_book_read(book)


def create_book(db: Session, payload: BookCreate) -> BookRead:
    _ensure_author_exists(db, payload.author_id)
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    stmt = select(Book).options(joinedload(Book.author)).where(Book.id == book.id)
    loaded_book = db.scalar(stmt)
    return to_book_read(loaded_book)


def update_book(db:Session, book_id:int, payload: BookUpdate) -> BookRead:
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    update_data = payload.model_dump(exclude_unset=True)
    if "author_id" in update_data:
        _ensure_author_exists(db, update_data["author_id"])
    for key, value in update_data.items():
        setattr(book, key, value)
    db.commit()
    stmt = select(Book).options(joinedload(Book.author)).where(Book.id == book.id)
    loaded_book = db.scalar(stmt)
    return to_book_read(loaded_book)


def delete_book(db: Session, book_id: int) -> None:
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()


def list_books_by_author(db: Session, author_id: int) -> list[BookRead]:
    _ensure_author_exists(db, author_id)
    stmt = select(Book).options(joinedload(Book.author)).where(Book.author_id == author_id)
    books = db.scalars(stmt).all()
    return [to_book_read(book) for book in books]