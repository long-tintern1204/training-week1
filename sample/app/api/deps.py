"""
FILE: app/api/deps.py
MỤC ĐÍCH:
- Chứa các hàm DEPENDENCY INJECTION phục vụ xác thực người dùng và phân quyền (RBAC).
- Trích xuất token từ Header, kiểm tra tính hợp lệ của JWT, lấy User hiện tại và kiểm tra quyền Admin.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Sử dụng `get_settings()` từ `app/core/config.py` để lấy `secret_key` giải mã token.
- Sử dụng `get_db` từ `app/db/session.py` để truy vấn thông tin User trong DB.
- Sử dụng `get_user_by_username` từ `app/services/user_service.py` để tìm User.
- Được sử dụng trong các Router (`app/api/routers/books.py`, `app/api/routers/users.py`, `app/api/routers/auth.py`)
  thông qua `Depends(get_current_user)` hoặc `Depends(get_current_admin)`.
"""

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models import User
from app.services.user_service import get_user_by_username

# OAuth2PasswordBearer giúp FastAPI tự động tìm Header: "Authorization: Bearer <token>"
# và hiển thị nút "Authorize" (ổ khóa) trên Swagger UI (/docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency: Xác thực và lấy đối tượng User hiện tại từ JWT token gửi kèm trong Request Header.
    
    Quy trình:
    1. Đọc chuỗi `token` từ Header `Authorization`.
    2. Dùng thư viện PyJWT để giải mã token với `secret_key` và thuật toán `HS256`.
    3. Lấy `username` từ payload (`sub`).
    4. Tìm User trong Database.
    5. Nếu token sai, hết hạn hoặc không tìm thấy user -> Ném lỗi 401 Unauthorized.
    6. Nếu hợp lệ -> Trả về instance `User` để router sử dụng.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency: Kiểm tra xem User hiện tại có phải là Admin hay không.
    
    Quy trình:
    1. Kế thừa dependency `get_current_user` -> Đảm bảo user đã đăng nhập hợp lệ trước.
    2. Kiểm tra `current_user.role`:
       - Nếu `role != 0` (tức là user thường, role = 1) -> Ném lỗi 403 Forbidden ("Not enough permissions").
       - Nếu `role == 0` (Admin) -> Trả về `current_user` và cho phép thực thi API.
    """
    if current_user.role != 0:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return current_user