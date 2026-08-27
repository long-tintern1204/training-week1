# ==============================================================================
# TẬP TIN: app/services/author_service.py
# VAI TRÒ: Tầng xử lý logic nghiệp vụ và truy vấn CSDL cho Tác giả (Authors)
# LIÊN KẾT:
#   - Được gọi bởi Router: app/api/routers/authors.py
#   - Sử dụng Models: app/models/author.py (Author), app/models/book.py (Book)
#   - Sử dụng Schemas: app/schemas/author.py (AuthorCreate, AuthorUpdate)
# ==============================================================================

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Author, Book
from app.schemas.author import AuthorCreate, AuthorUpdate


def list_authors(db: Session) -> list[Author]:
    """
    Lấy danh sách tất cả tác giả trong CSDL, sắp xếp tăng dần theo ID.
    - select(Author): Tạo câu lệnh SELECT * FROM authors
    - db.scalars(stmt): Thực thi câu lệnh và trả về danh sách đối tượng Author
    """
    stmt = select(Author).order_by(Author.id)
    return list(db.scalars(stmt))


def get_author(db: Session, author_id: int) -> Author:
    """
    Lấy thông tin chi tiết một tác giả theo ID.
    - db.get(Author, author_id): Tìm bản ghi theo khóa chính (Primary Key).
    - Nếu không tìm thấy, văng lỗi HTTP 404 (Not Found).
    """
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_author(db: Session, payload: AuthorCreate) -> Author:
    """
    Tạo mới một tác giả.
    - payload.model_dump(): Chuyển đổi Pydantic model thành dict Python.
    - Author(**...): Đưa dữ liệu vào SQLAlchemy model.
    - db.add() -> db.commit(): Lưu bản ghi vào CSDL.
    - db.refresh(): Cập nhật lại đối tượng với ID vừa được database tự động tạo ra.
    """
    author = Author(**payload.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update_author(db: Session, author_id: int, payload: AuthorUpdate) -> Author:
    """
    Cập nhật thông tin tác giả theo ID.
    - exclude_unset=True: Chỉ lấy những trường mà client thực sự gửi lên.
    - setattr(author, key, value): Gán lại giá trị cho từng thuộc tính của model.
    """
    author = get_author(db, author_id)
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int) -> None:
    """
    Xóa một tác giả theo ID.
    LOGIC NGHIỆP VỤ ĐẶC BIỆT:
    - Trước khi xóa, đếm xem tác giả này có đang sở hữu cuốn sách nào không.
    - Nếu số lượng sách > 0: Văng lỗi HTTP 409 (Conflict), không cho phép xóa.
    - Nếu không có sách: Tiến hành xóa bản ghi khỏi CSDL.
    """
    author = get_author(db, author_id)
    stmt = select(func.count(Book.id)).where(Book.author_id == author_id)
    book_count = db.scalar(stmt)
    if book_count > 0:
        raise HTTPException(status_code=409, detail="Cannot delete author while books exist")
    db.delete(author)
    db.commit()