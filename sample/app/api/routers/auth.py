"""
FILE: app/api/routers/auth.py
MỤC ĐÍCH:
- Chứa các endpoint liên quan đến Xác thực (Authentication):
  1. `POST /api/v1/auth/login`: Đăng nhập bằng username/password để nhận JWT token.
  2. `GET /api/v1/auth/me`: Lấy thông tin tài khoản hiện đang đăng nhập từ JWT token.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Nhận dữ liệu input qua Schema `LoginRequest` và trả về qua `Token`, `UserRead` (`app/schemas/user.py`).
- Cung cấp DB session thông qua `get_db` (`app/db/session.py`).
- Gọi logic đăng nhập từ `user_service.login` (`app/services/user_service.py`).
- Sử dụng dependency `get_current_user` (`app/api/deps.py`) để bảo vệ endpoint `/me`.
- Được gắn vào ứng dụng chính trong `app/main.py` với tiền tố `/api/v1`.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.user import LoginRequest, Token, UserRead
from app.services import user_service

# Khởi tạo Router với prefix="/auth" và gắn tag để nhóm trên Swagger docs
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    """
    API Đăng nhập:
    - Input: JSON body gồm `username` và `password`.
    - Xử lý: `user_service.login()` kiểm tra password và tạo chuỗi JWT Access Token.
    - Output: Object `{ "access_token": "...", "token_type": "bearer" }`.
    """
    token = user_service.login(db, payload.username, payload.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """
    API Lấy thông tin User hiện tại:
    - Yêu cầu Header: `Authorization: Bearer <token>`.
    - Dependency `get_current_user` tự động giải mã token và lấy user từ DB.
    - Output: Thông tin user `{ "id": 1, "username": "admin", "role": 0 }` (không có mật khẩu).
    """
    return current_user