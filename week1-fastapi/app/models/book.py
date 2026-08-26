"""
File: app/models/book.py
Mục đích: Định nghĩa SQLAlchemy ORM Model cho bảng 'books' (Sách).

Liên kết với các file khác:
- app/database.py: Import lớp `Base` để kế thừa.
- app/models/author.py: Cột `author_id` thiết lập khoá ngoại liên kết tới `authors.id`.
- app/models/__init__.py: Re-export model `Book`.
- app/admin.py: Dùng để cấu hình hiển thị quản trị `BookAdmin` trên SQLAdmin.
- main.py: Dùng để thực hiện các thao tác CRUD với Sách (`db.query(Book)`, `db.get(Book, ...)`).
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    # Tên bảng thực tế trong Database SQLite
    __tablename__ = "books"

    # Cột 'id': Khóa chính (primary key), tự động tăng, được đánh index
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Cột 'title': Tiêu đề sách, chuỗi tối đa 200 ký tự, không được để trống (nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Cột 'year': Năm xuất bản, kiểu số nguyên, bắt buộc phải có
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Cột 'summary': Tóm tắt nội dung sách, tối đa 500 ký tự, có thể để trống (nullable=True, mặc định None)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Cột 'author_id': Khoá ngoại (ForeignKey) trỏ đến 'authors.id' (bảng authors cột id)
    # Có thể để trống (nullable=True) nếu sách chưa rõ tác giả
    author_id: Mapped[int | None] = mapped_column(ForeignKey("authors.id"), nullable=True)
