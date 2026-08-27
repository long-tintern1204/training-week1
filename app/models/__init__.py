# ==============================================================================
# TẬP TIN: app/models/__init__.py
# VAI TRÒ: Gom và xuất (export) toàn bộ SQLAlchemy Models tại một điểm duy nhất
# LIÊN KẾT:
#   - Giúp app/main.py, app/admin.py, alembic/env.py chỉ cần import từ 'app.models'
#   - Đảm bảo tất cả Model đều được nạp vào Base.metadata khi ứng dụng khởi động
# ==============================================================================

from app.models.author import Author
from app.models.book import Book
from app.models.category import Category


__all__ = ["Author", "Book", "Category"]