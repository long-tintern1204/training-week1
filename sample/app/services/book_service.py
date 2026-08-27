"""
FILE: app/services/book_service.py
MỤC ĐÍCH:
- Chứa toàn bộ LOGIC NGHIỆP VỤ (Business Logic) và các thao tác Database liên quan đến Sách (Books).
- Tách biệt logic khỏi Router giúp code gọn gàng, dễ bảo trì và dễ viết unit test.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Nhận dữ liệu input từ `app/schemas/book.py` (`BookCreate`, `BookUpdate`).
- Tương tác với Database thông qua ORM Model `Book` (`app/models/book.py`) và `Session` (`app/db/session.py`).
- Được gọi bởi các endpoint trong Router `app/api/routers/books.py`.
"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Book
from app.schemas.book import BookCreate, BookUpdate


def list_books(db: Session) -> list[Book]:
    """
    Lấy danh sách tất cả các cuốn sách trong Database, sắp xếp theo ID tăng dần.
    - SQL tương đương: SELECT * FROM books ORDER BY books.id ASC;
    """
    stmt = select(Book).order_by(Book.id)
    return list(db.scalars(stmt))


def get_book(db: Session, book_id: int) -> Book:
    """
    Tìm cuốn sách theo ID (khóa chính).
    - Nếu không tìm thấy: Ném lỗi HTTP 404 Not Found.
    - Nếu tìm thấy: Trả về đối tượng Book.
    """
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def create_book(db: Session, payload: BookCreate) -> Book:
    """
    Thêm một cuốn sách mới vào cơ sở dữ liệu.
    - `payload.model_dump()`: Chuyển dữ liệu từ Pydantic Schema thành dictionary.
    - `Book(**...)`: Khởi tạo instance của SQLAlchemy Model Book.
    - `db.add(...)`: Đưa đối tượng vào hàng đợi lưu của session.
    - `db.commit()`: Ghi thay đổi vĩnh viễn vào SQLite.
    - `db.refresh(...)`: Cập nhật lại đối tượng để lấy giá trị ID vừa được tự động sinh trong DB.
    """
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, payload: BookUpdate) -> Book:
    """
    Cập nhật thông tin cuốn sách theo ID.
    - B1: Tìm sách (nếu không thấy sẽ bị ngắt bởi hàm get_book với lỗi 404).
    - B2: Gán đè các thuộc tính mới từ payload vào đối tượng Book.
    - B3: Commit và refresh để lưu thay đổi.
    """
    book = get_book(db, book_id)
    for key, value in payload.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> None:
    """
    Xóa một cuốn sách khỏi cơ sở dữ liệu theo ID.
    - B1: Tìm sách (ném lỗi 404 nếu không tồn tại).
    - B2: Xóa đối tượng khỏi DB và commit.
    """
    book = get_book(db, book_id)
    db.delete(book)
    db.commit()
