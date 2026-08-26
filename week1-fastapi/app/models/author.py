"""
File: app/models/author.py
Mục đích: Định nghĩa SQLAlchemy ORM Model cho bảng 'authors' (Tác giả).

Liên kết với các file khác:
- app/database.py: Import lớp `Base` để kế thừa và đăng ký bảng vào SQLAlchemy Metadata.
- app/models/book.py: Model `Book` có khoá ngoại `ForeignKey("authors.id")` trỏ đến trường `id` của bảng này.
- app/models/__init__.py: Re-export model `Author` để dễ dàng import ở nơi khác.
- app/admin.py: Dùng để cấu hình hiển thị quản trị `AuthorAdmin` trên SQLAdmin.
- main.py: Dùng để truy vấn kiểm tra tác giả tồn tại (`db.get(Author, payload.author_id)`).
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Author(Base):
    # Tên bảng thực tế trong Database SQLite
    __tablename__ = "authors"
    
    # Cột 'id': Kiểu số nguyên (Integer), là khoá chính (primary_key=True), được đánh chỉ mục tìm kiếm (index=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Cột 'name': Tên tác giả, chuỗi tối đa 200 ký tự (String(200)), bắt buộc phải có (nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)