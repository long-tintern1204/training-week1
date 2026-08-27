"""
FILE: app/api/routers/users.py
MỤC ĐÍCH:
- Chứa các RESTful API endpoints liên quan đến Người dùng (Users).
- Thiết lập quyền hạn (Authorization):
  + POST /users (Đăng ký tài khoản): Công khai.
  + GET /users, GET /users/{id}: Công khai.
  + PUT /users/{id}, DELETE /users/{id}: Bắt buộc quyền ADMIN (role = 0).

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Nhận input / Trả về output qua Schemas: `UserCreate`, `UserRead`, `UserUpdate` (`app/schemas/user.py`).
- Nhận DB session từ `get_db` (`app/db/session.py`).
- Kiểm tra quyền Admin qua dependency `get_current_admin` (`app/api/deps.py`).
- Gọi các hàm xử lý logic từ `app/services/user_service.py`.
- Được gắn vào ứng dụng chính trong `app/main.py` với tiền tố `/api/v1`.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter(tags=["users"])


@router.post("/users", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """
    Tạo tài khoản / Đăng ký người dùng mới (Public).
    - Mật khẩu sẽ được băm tự động trong user_service trước khi lưu vào DB.
    """
    return user_service.create_user(db, payload)


@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)) -> list[UserRead]:
    """
    Lấy danh sách tất cả người dùng trong hệ thống (Public).
    - Response chỉ trả về id, username, role (không có password).
    """
    return user_service.list_users(db)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    """
    Lấy thông tin chi tiết của 1 người dùng theo ID (Public).
    """
    return user_service.get_user(db, user_id)


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # Bắt buộc phải là Admin
) -> UserRead:
    """
    Cập nhật thông tin người dùng (Chỉ ADMIN mới có quyền).
    """
    return user_service.update_user(db, user_id, payload)


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # Bắt buộc phải là Admin
) -> None:
    """
    Xóa tài khoản người dùng (Chỉ ADMIN mới có quyền, trả về status code 204).
    """
    user_service.delete_user(db, user_id)
