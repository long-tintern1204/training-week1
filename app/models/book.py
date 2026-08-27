# ==============================================================================
# TẬP TIN: app/models/book.py
# VAI TRÒ: Định nghĩa cấu trúc bảng 'books' trong CSDL (SQLAlchemy ORM Model)
# LIÊN KẾT:
#   - Kế thừa Base từ: app/db/database.py
#   - Khóa ngoại liên kết tới bảng 'authors' (app/models/author.py)
#   - Khóa ngoại liên kết tới bảng 'categories' (app/models/category.py)
#   - Được sử dụng bởi: app/services/book_service.py, app/admin.py, alembic
# ==============================================================================

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Book(Base):
    """
    Model đại diện cho bảng 'books' lưu trữ thông tin Sách trong CSDL.
    """
    __tablename__ = "books"
    
    # Khóa chính tự tăng
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Tiêu đề sách, bắt buộc có
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Năm xuất bản, bắt buộc có
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Tóm tắt nội dung sách, tối đa 500 ký tự, có thể để trống
    summary: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Khóa ngoại trỏ đến cột id của bảng authors (có thể để None nếu chưa gán tác giả)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("authors.id"), nullable=True)
    
    # ORM Relationship: Giúp truy cập trực tiếp đối tượng Author của cuốn sách qua book.author
    author = relationship("Author", back_populates="books")
    
    # Khóa ngoại trỏ đến cột id của bảng categories (có thể để None nếu chưa gán thể loại)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    
    # ORM Relationship: Giúp truy cập trực tiếp đối tượng Category của cuốn sách qua book.category
    category = relationship("Category", back_populates="books")