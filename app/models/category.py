# ==============================================================================
# TẬP TIN: app/models/category.py
# VAI TRÒ: Định nghĩa cấu trúc bảng 'categories' trong CSDL (SQLAlchemy ORM Model)
# LIÊN KẾT:
#   - Kế thừa Base từ: app/db/database.py
#   - Thiết lập quan hệ 1-N (One-to-Many) với Book: app/models/book.py
#   - Được sử dụng bởi: app/services/category_service.py, app/admin.py, alembic
# ==============================================================================

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Category(Base):
    """
    Model đại diện cho bảng 'categories' lưu thông tin Thể loại/Danh mục sách trong CSDL.
    """
    __tablename__ = "categories"

    # Khóa chính tự tăng
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) 
    
    # Tên danh mục (ví dụ: "Khoa học", "Công nghệ", "Văn học"), bắt buộc có
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Quan hệ 1-N: Một thể loại có thể chứa nhiều cuốn sách
    # back_populates="category" liên kết ngược lại với thuộc tính 'category' trong model Book
    books = relationship("Book", back_populates="category")