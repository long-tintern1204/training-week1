"""
FILE: app/main.py
MỤC ĐÍCH:
- ĐÂY LÀ ENTRY POINT (ĐIỂM KHỞI CHẠY CHÍNH) CỦA TOÀN BỘ PROJECT BACKEND.
- Khởi tạo ứng dụng FastAPI, cấu hình CORS Middleware.
- Tự động tạo bảng cơ sở dữ liệu nếu chưa có.
- Khởi tạo giao diện SQLAdmin.
- Đăng ký (include) các API router: `books`, `users`, `auth` với tiền tố chung `/api/v1`.

CÁCH CHẠY DỰ ÁN:
- Chạy lệnh: `uvicorn app.main:app --reload`
- Swagger UI (tài liệu tương tác API): http://127.0.0.1:8000/docs
- Admin Dashboard: http://127.0.0.1:8000/admin
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin import setup_admin
from app.api.routers import books, users, auth
from app.core.config import get_settings
from app.db.database import Base
from app.db.session import engine
from app.models import Book, User  # noqa: F401 - Import để Base.metadata nhận diện được các Model

# 1. Đọc cấu hình từ file .env
settings = get_settings()

# 2. Khởi tạo instance FastAPI
app = FastAPI(title=settings.app_title)

# 3. Cấu hình Middleware CORS (Cross-Origin Resource Sharing)
# Cho phép ứng dụng Frontend (chạy tại cổng 5173 - Vite) có thể gọi API tới Backend này
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Front-end Vite chạy qua localhost
        "http://127.0.0.1:5173",  # Front-end Vite chạy qua IP loopback
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả HTTP methods (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # Cho phép tất cả Headers (bao gồm Authorization Header)
)

# 4. Tự động tạo các bảng trong Database SQLite nếu chưa tồn tại
Base.metadata.create_all(bind=engine)

# 5. Cấu hình SQLAdmin UI tại đường dẫn /admin
setup_admin(app, engine)

# 6. Gắn các Router API vào ứng dụng với tiền tố prefix="/api/v1"
app.include_router(books.router, prefix="/api/v1")  # Các route: /api/v1/books, /api/v1/books/{id}
app.include_router(users.router, prefix="/api/v1")  # Các route: /api/v1/users, /api/v1/users/{id}
app.include_router(auth.router, prefix="/api/v1")   # Các route: /api/v1/auth/login, /api/v1/auth/me


# 7. Endpoint kiểm tra trạng thái hoạt động (Health check / Root)
@app.get("/")
def root() -> dict[str, str]:
    """
    Endpoint gốc kiểm tra server có đang chạy bình thường hay không.
    - Truy cập: http://127.0.0.1:8000/
    """
    return {"message": "Hello World"}
