"""
FILE: app/db/session.py
MỤC ĐÍCH:
- Khởi tạo SQLAlchemy `Engine` và nhà máy tạo session `SessionLocal`.
- Cung cấp hàm dependency `get_db()` để quản lý vòng đời (mở/đóng) kết nối DB theo từng request.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Nhận `DATABASE_URL` từ `app/db/database.py`.
- Cung cấp `engine` cho `app/main.py` (tạo bảng và cấu hình SQLAdmin) và `app/admin.py`.
- Cung cấp hàm `get_db()` cho các Router (`app/api/routers/*.py`) và Dependency (`app/api/deps.py`) thông qua `Depends(get_db)`.
"""

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import DATABASE_URL

# Khởi tạo kết nối DB Engine
# connect_args={"check_same_thread": False} là cấu hình bắt buộc khi dùng SQLite với ứng dụng đa luồng (FastAPI)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal là một class factory dùng để tạo ra các Database Session độc lập
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI Dependency: Tạo và cung cấp DB Session cho mỗi HTTP Request.
    - `yield db`: Cung cấp session cho Router/Service xử lý truy vấn.
    - `finally: db.close()`: Đảm bảo session luôn được đóng sau khi request hoàn tất,
      tránh hiện tượng rò rỉ kết nối (connection leak).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
