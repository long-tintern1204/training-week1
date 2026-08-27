"""
FILE: app/api/routers/books.py
MỤC ĐÍCH:
- Chứa toàn bộ các RESTful API endpoints liên quan đến Sách (Books).
- Thiết lập quyền hạn (Authorization) cho từng thao tác:
  + GET /books, GET /books/{id}: Công khai (Ai cũng xem được).
  + POST /books: Yêu cầu ĐĂNG NHẬP (User thường hoặc Admin).
  + PUT /books/{id}, DELETE /books/{id}: Bắt buộc quyền ADMIN (role = 0).

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Nhận input / Trả về output qua Schemas: `BookCreate`, `BookRead`, `BookUpdate` (`app/schemas/book.py`).
- Nhận DB session từ `get_db` (`app/db/session.py`).
- Xác thực quyền qua dependencies: `get_current_user`, `get_current_admin` (`app/api/deps.py`).
- Gọi các hàm nghiệp vụ trong `app/services/book_service.py`.
- Được gắn vào ứng dụng chính trong `app/main.py` với tiền tố `/api/v1`.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services import book_service

router = APIRouter(tags=["books"])


@router.get("/books", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)) -> list[BookRead]:
    """
    Lấy danh sách tất cả sách (Public - Không cần đăng nhập).
    """
    return book_service.list_books(db)


@router.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookRead:
    """
    Lấy chi tiết 1 cuốn sách theo ID (Public - Không cần đăng nhập).
    """
    return book_service.get_book(db, book_id)


@router.post("/books", response_model=BookRead, status_code=201)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Bắt buộc phải có token hợp lệ
) -> BookRead:
    """
    Thêm sách mới (Bắt buộc ĐĂNG NHẬP - Bất kể role nào).
    """
    return book_service.create_book(db, payload)


@router.put("/books/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # Bắt buộc phải là Admin (role = 0)
) -> BookRead:
    """
    Cập nhật thông tin sách (Chỉ ADMIN mới có quyền).
    """
    return book_service.update_book(db, book_id, payload)


@router.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # Bắt buộc phải là Admin (role = 0)
) -> None:
    """
    Xóa sách theo ID (Chỉ ADMIN mới có quyền, trả về status code 204 No Content).
    """
    book_service.delete_book(db, book_id)
