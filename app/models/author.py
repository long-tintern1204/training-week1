# ==============================================================================
# TẬP TIN: app/models/author.py
# VAI TRÒ: Định nghĩa cấu trúc bảng 'authors' trong CSDL (SQLAlchemy ORM Model)
# LIÊN KẾT:
#   - Kế thừa Base từ: app/db/database.py
#   - Thiết lập quan hệ 1-N (One-to-Many) với Book: app/models/book.py
#   - Được sử dụng bởi: app/services/author_service.py, app/admin.py, alembic
# ==============================================================================

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Author(Base):
    """
    Model đại diện cho bảng 'authors' lưu thông tin Tác giả trong CSDL.
    Sử dụng cú pháp Mapped[...] hiện đại của SQLAlchemy 2.0.
    """
    __tablename__ = "authors"

    # Khóa chính tự tăng (Primary Key), có đánh index để tìm kiếm nhanh
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Tên tác giả: kiểu chuỗi tối đa 200 ký tự, bắt buộc phải có (nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Tiểu sử tác giả: tối đa 1000 ký tự, có thể để trống (nullable=True)
    bio: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    # Quốc gia: tối đa 100 ký tự, có thể để trống
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Năm sinh: số nguyên, có thể để trống
    birth_year: Mapped[int] = mapped_column(Integer, nullable=True)

    # Quan hệ 1-N: Một tác giả có thể có nhiều cuốn sách (list các đối tượng Book)
    # back_populates="author" liên kết ngược lại với thuộc tính 'author' trong model Book
    books = relationship("Book", back_populates="author")