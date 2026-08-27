# ==============================================================================
# TẬP TIN: app/db/session.py
# VAI TRÒ: Quản lý Engine kết nối và cung cấp phiên làm việc (Session) với CSDL
# LIÊN KẾT:
#   - Nhận DATABASE_URL từ: app/db/database.py
#   - Cung cấp engine cho: app/main.py, app/admin.py
#   - Cung cấp get_db() dependency cho: tất cả API Routers trong app/api/routers/*.py
# ==============================================================================

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import DATABASE_URL

# Khởi tạo SQLAlchemy Engine: Cầu nối thực tế giữa ứng dụng Python và cơ sở dữ liệu SQLite
# check_same_thread: False là bắt buộc đối với SQLite khi chạy trong môi trường đa luồng (multi-thread) của FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Factory tạo ra các Session (phiên làm việc độc lập với CSDL cho mỗi request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency Injection function dùng trong FastAPI routers.
    - Mỗi khi có một Request đến API, hàm này tạo một Session mới (`db = SessionLocal()`).
    - `yield db`: Cung cấp session cho Router/Service sử dụng.
    - `finally: db.close()`: Đảm bảo luôn luôn đóng kết nối giải phóng tài nguyên sau khi request kết thúc,
      kể cả khi xảy ra lỗi trong quá trình xử lý.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
