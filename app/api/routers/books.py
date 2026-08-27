# ==============================================================================
# TẬP TIN: app/api/routers/books.py
# VAI TRÒ: Tầng tiếp nhận HTTP Request và trả về Response cho Sách (Books API)
# ĐƯỜNG DẪN: /api/v1/books, /api/v1/search/books, /api/v1/authors/{id}/books
# LIÊN KẾT:
#   - Nhận DB Session từ: app/db/session.py (get_db)
#   - Validate dữ liệu với: app/schemas/book.py (BookCreate, BookRead, BookUpdate)
#   - Chuyển giao logic cho: app/services/book_service.py
# ==============================================================================

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services import book_service

# Khởi tạo Router cho Sách với tag "books" trong Swagger Docs
router = APIRouter(tags=["books"])


@router.get("/books", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)) -> list[BookRead]:
    """
    [GET] /api/v1/books
    Lấy danh sách tất cả các cuốn sách kèm tên tác giả và tên thể loại.
    """
    return book_service.list_books(db)


@router.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookRead:
    """
    [GET] /api/v1/books/{book_id}
    Lấy thông tin chi tiết một cuốn sách theo ID.
    """
    return book_service.get_book(db, book_id)


@router.get("/search/books", response_model=list[BookRead])
def search_books(
    db: Session = Depends(get_db),
    author_id: int | None = Query(default=None, description="Lọc theo ID tác giả"),
    category_id: int | None = Query(default=None, description="Lọc theo ID danh mục"),
    year_from: int | None = Query(default=None, description="Lọc sách xuất bản từ năm"),
    year_to: int | None = Query(default=None, description="Lọc sách xuất bản đến năm"),
    q: str | None = Query(default=None, description="Tìm kiếm từ khóa theo tiêu đề sách"),
) -> list[BookRead]:
    """
    [GET] /api/v1/search/books
    Tìm kiếm sách linh hoạt thông qua các Query Parameters trên URL:
    Ví dụ: /api/v1/search/books?year_from=2000&q=python
    """
    return book_service.search_books(
        db,
        author_id=author_id,
        category_id=category_id,
        year_from=year_from,
        year_to=year_to,
        q=q,
    )


@router.post("/books", response_model=BookRead, status_code=201)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
) -> BookRead:
    """
    [POST] /api/v1/books
    Tạo mới một cuốn sách.
    """
    return book_service.create_book(db, payload)


@router.put("/books/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
) -> BookRead:
    """
    [PUT] /api/v1/books/{book_id}
    Cập nhật thông tin cuốn sách theo ID.
    """
    return book_service.update_book(db, book_id, payload)


@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    """
    [DELETE] /api/v1/books/{book_id}
    Xóa một cuốn sách theo ID.
    """
    return book_service.delete_book(db, book_id)


@router.get("/authors/{author_id}/books", response_model=list[BookRead])
def list_books_by_author(
    author_id: int,
    db: Session = Depends(get_db),
) -> list[BookRead]:
    """
    [GET] /api/v1/authors/{author_id}/books
    Lấy danh sách tất cả các cuốn sách được viết bởi một tác giả cụ thể.
    """
    return book_service.list_books_by_author(db, author_id)