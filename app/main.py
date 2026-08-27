# ==============================================================================
# TẬP TIN: app/main.py
# VAI TRÒ: Điểm khởi chạy (Entry Point) của toàn bộ ứng dụng FastAPI
# CÁCH CHẠY: uvicorn app.main:app --reload
# LIÊN KẾT:
#   - Khởi tạo FastAPI app với tiêu đề từ: app/core/config.py
#   - Tự động tạo bảng CSDL từ: app/db/database.py (Base) & app/db/session.py (engine)
#   - Tích hợp giao diện quản trị từ: app/admin.py (setup_admin)
#   - Gắn các router API từ: app/api/routers/ (authors, books, categories)
# ==============================================================================

from fastapi import FastAPI

from app.admin import setup_admin
from app.core.config import get_settings
from app.db.database import Base
from app.db.session import engine
from app.api.routers import authors, books, categories
from app.models import Author, Book, Category

# 1. Đọc cấu hình ứng dụng
settings = get_settings()

# 2. Khởi tạo đối tượng ứng dụng FastAPI
app = FastAPI(title=settings.app_title)

# 3. Tự động tạo bảng trong Database SQLite nếu chưa tồn tại (dựa trên metadata của Base)
Base.metadata.create_all(bind=engine)

# 4. Thiết lập trang quản trị trực quan SQLAdmin tại đường dẫn /admin
setup_admin(app, engine)

# 5. Đăng ký các router với tiền tố chung là /api/v1
app.include_router(authors.router, prefix="/api/v1")
app.include_router(books.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    """
    Endpoint kiểm tra trạng thái hoạt động của server (Health Check / Welcome).
    """
    return {"message": "Hello World"}
