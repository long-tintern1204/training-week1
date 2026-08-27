# ==============================================================================
# TẬP TIN: app/services/book_service.py
# VAI TRÒ: Tầng xử lý logic nghiệp vụ và truy vấn CSDL cho Sách (Books)
# LIÊN KẾT:
#   - Được gọi bởi Router: app/api/routers/books.py
#   - Sử dụng Models: app/models/book.py (Book), app/models/author.py (Author), app/models/category.py (Category)
#   - Sử dụng Schemas: app/schemas/book.py (BookCreate, BookUpdate, BookRead)
# ==============================================================================

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Author, Book, Category
from app.schemas.book import BookCreate, BookRead, BookUpdate


def to_book_read(book: Book) -> BookRead:
    """
    Hàm tiện ích (Helper Function):
    Chuyển đổi đối tượng ORM Model `Book` thành Schema DTO `BookRead`.
    Tự động lấy `author.name` và `category.name` nếu các quan hệ này tồn tại.
    """
    return BookRead(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        author_name=book.author.name if book.author else None,
        summary=book.summary,
        year=book.year,
        category_id=book.category_id,
        category_name=book.category.name if book.category else None
    )


def _ensure_author_exists(db: Session, author_id: int | None) -> None:
    """
    Hàm kiểm tra tính hợp lệ của Tác giả (Foreign Key Validation):
    - Nếu `author_id` là None: Bỏ qua (cho phép sách chưa có tác giả).
    - Nếu có `author_id` nhưng không tìm thấy trong bảng `authors`: Văng lỗi HTTP 404.
    """
    if author_id is None:
        return
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    
def _ensure_category_exists(db: Session, category_id: int | None) -> None:
    """
    Hàm kiểm tra tính hợp lệ của Thể loại (Foreign Key Validation):
    - Nếu `category_id` là None: Bỏ qua (cho phép sách chưa có thể loại).
    - Nếu có `category_id` nhưng không tìm thấy trong bảng `categories`: Văng lỗi HTTP 404.
    """
    if category_id is None:
        return
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")    
    
    
def list_books(db: Session) -> list[BookRead]:
    """
    Lấy danh sách tất cả sách kèm thông tin Tác giả và Danh mục.
    - joinedload(Book.author), joinedload(Book.category): Kỹ thuật Eager Loading trong SQLAlchemy,
      giúp nạp trước dữ liệu quan hệ trong 1 câu SQL JOIN duy nhất, tránh vấn đề N+1 Query.
    """
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category)
    )
    books = db.scalars(stmt).all()
    return [to_book_read(book) for book in books]


def get_book(db: Session, book_id: int) -> BookRead:
    """
    Lấy thông tin chi tiết của 1 cuốn sách theo ID kèm quan hệ.
    """
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category)
    ).where(Book.id == book_id)
    book = db.scalar(stmt)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return to_book_read(book)


def create_book(db: Session, payload: BookCreate) -> BookRead:
    """
    Tạo mới một cuốn sách.
    Quy trình:
    1. Kiểm tra author_id và category_id có hợp lệ trong CSDL không.
    2. Lưu bản ghi vào database.
    3. Query lại cuốn sách vừa tạo kèm quan hệ (joinedload) để trả về đầy đủ author_name & category_name.
    """
    _ensure_author_exists(db, payload.author_id)
    _ensure_category_exists(db, payload.category_id)
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category)
    ).where(Book.id == book.id)
    loaded_book = db.scalar(stmt)
    return to_book_read(loaded_book)


def update_book(db: Session, book_id: int, payload: BookUpdate) -> BookRead:
    """
    Cập nhật thông tin sách theo ID.
    1. Kiểm tra sách có tồn tại không.
    2. Kiểm tra author_id / category_id mới có hợp lệ không (nếu có cập nhật).
    3. Cập nhật các trường dữ liệu và commit vào CSDL.
    4. Query lại kèm quan hệ để trả về BookRead đầy đủ.
    """
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    update_data = payload.model_dump(exclude_unset=True)
    if "author_id" in update_data:
        _ensure_author_exists(db, update_data["author_id"])
    if "category_id" in update_data:
        _ensure_category_exists(db, update_data["category_id"])
    for key, value in update_data.items():
        setattr(book, key, value)
    db.commit()
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category)
    ).where(Book.id == book.id)
    loaded_book = db.scalar(stmt)
    return to_book_read(loaded_book)


def delete_book(db: Session, book_id: int) -> None:
    """
    Xóa một cuốn sách theo ID.
    """
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()


def list_books_by_author(db: Session, author_id: int) -> list[BookRead]:
    """
    Lấy danh sách tất cả các cuốn sách thuộc về một Tác giả cụ thể.
    """
    _ensure_author_exists(db, author_id)
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category)
    ).where(Book.author_id == author_id)
    books = db.scalars(stmt).all()
    return [to_book_read(book) for book in books]


def search_books(
    db: Session,
    *,
    author_id: int | None = None,
    category_id: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    q: str | None = None,
) -> list[BookRead]:
    """
    Tìm kiếm sách linh hoạt với nhiều tiêu chí lọc:
    - author_id: Lọc theo tác giả
    - category_id: Lọc theo danh mục
    - year_from / year_to: Lọc theo khoảng năm xuất bản (>= year_from và <= year_to)
    - q: Tìm kiếm tương đối theo tiêu đề sách (không phân biệt chữ hoa/thường qua ilike)
    """
    stmt = select(Book).options(
        joinedload(Book.author),
        joinedload(Book.category),
    )
    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)
    if category_id is not None:
        stmt = stmt.where(Book.category_id == category_id)
    if year_from is not None:
        stmt = stmt.where(Book.year >= year_from)
    if year_to is not None:
        stmt = stmt.where(Book.year <= year_to)
    if q:
        stmt = stmt.where(Book.title.ilike(f"%{q}%"))

    stmt = stmt.order_by(Book.id)
    books = db.scalars(stmt).all()
    return [to_book_read(book) for book in books]