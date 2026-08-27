"""
FILE: app/models/book.py
MỤC ĐÍCH:
- Khai báo ORM Model `Book`, ánh xạ trực tiếp thành bảng `books` trong Database.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Kế thừa `Base` từ `app/db/database.py`.
- Được import bởi `app/models/__init__.py` để gom nhóm các model.
- Được sử dụng bởi `app/services/book_service.py` để thực hiện câu lệnh truy vấn (SELECT, INSERT, UPDATE, DELETE).
- Được sử dụng bởi `app/admin.py` để hiển thị dữ liệu sách lên trang quản trị SQLAdmin.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Book(Base):
    """
    Bảng 'books' lưu thông tin sách:
    - id: Khóa chính (Primary Key), tự tăng.
    - title: Tên sách (tối đa 200 ký tự, không được để trống).
    - year: Năm xuất bản (số nguyên, không được để trống).
    - summary: Tóm tắt nội dung sách (tối đa 500 ký tự, có thể để trống / null).
    """
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
