"""
FILE: app/db/database.py
MỤC ĐÍCH:
- Xác định đường dẫn lưu trữ cơ sở dữ liệu SQLite và URL kết nối.
- Khai báo lớp `Base` (DeclarativeBase) - lớp cha của tất cả các ORM Model trong dự án.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Lấy cấu hình `database_url` từ `app/core/config.py`.
- Cung cấp `DATABASE_URL` cho `app/db/session.py` để khởi tạo SQLAlchemy Engine.
- Cung cấp `Base` cho các file models: `app/models/book.py` và `app/models/user.py`.
- Cung cấp `Base` cho `app/main.py` để chạy lệnh tạo bảng: `Base.metadata.create_all(bind=engine)`.
- Cung cấp `Base` cho Alembic trong `alembic/env.py` để theo dõi thay đổi bảng (migrations).
"""

from pathlib import Path
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

# Định nghĩa đường dẫn thư mục `data/` nằm ở thư mục gốc của project
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)  # Tự động tạo thư mục data nếu chưa tồn tại

settings = get_settings()

# Nếu trong .env có DATABASE_URL thì dùng URL đó, nếu không sẽ dùng SQLite lưu tại data/books.db
DATABASE_URL = settings.database_url or f"sqlite:///{DATA_DIR / 'books.db'}"


class Base(DeclarativeBase):
    """
    Lớp cơ sở của SQLAlchemy (DeclarativeBase).
    Tất cả các Model (Book, User...) đều phải kế thừa từ lớp này để SQLAlchemy nhận diện là bảng trong DB.
    """
    pass
