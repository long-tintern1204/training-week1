"""
FILE: app/models/__init__.py
MỤC ĐÍCH:
- Gom tất cả các model lại một chỗ để tiện import từ bên ngoài (ví dụ: `from app.models import Book, User`).
- Giúp SQLAlchemy và Alembic nhận diện đầy đủ tất cả các bảng khi load metadata.
"""

from app.models.book import Book
from app.models.user import User


__all__ = ["Book", "User"]