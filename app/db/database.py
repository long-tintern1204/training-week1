# ==============================================================================
# TẬP TIN: app/db/database.py
# VAI TRÒ: Khởi tạo Base ORM và cấu hình đường dẫn kết nối CSDL (DATABASE_URL)
# LIÊN KẾT:
#   - Nhận cấu hình từ: app/core/config.py
#   - Cung cấp Base cho: app/models/*.py, alembic/env.py, app/main.py
#   - Cung cấp DATABASE_URL cho: app/db/session.py, alembic/env.py
# ==============================================================================

from pathlib import Path
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

# Xác định đường dẫn tuyệt đối đến thư mục 'data' ở thư mục gốc của project
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
# Tự động tạo thư mục 'data' nếu thư mục này chưa tồn tại
DATA_DIR.mkdir(exist_ok=True)

# Lấy cấu hình từ Settings
settings = get_settings()

# Nếu trong file .env có cấu hình database_url thì dùng, ngược lại dùng SQLite lưu tại data/books.db
DATABASE_URL = settings.database_url or f"sqlite:///{DATA_DIR / 'books.db'}"


class Base(DeclarativeBase):
    """
    Lớp cơ sở (Base Class) cho tất cả các ORM Models trong dự án (SQLAlchemy 2.0).
    Tất cả các Model như Author, Book, Category đều phải kế thừa từ Base này
    để SQLAlchemy nhận biết và quản lý metadata các bảng trong CSDL.
    """
    pass
