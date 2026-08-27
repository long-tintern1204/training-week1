"""
FILE: app/services/user_service.py
MỤC ĐÍCH:
- Chứa toàn bộ LOGIC NGHIỆP VỤ và thao tác Database liên quan đến Người dùng (Users) và Đăng nhập (Auth).
- Xử lý kiểm tra trùng lặp username, mã hóa mật khẩu, kiểm tra đăng nhập và sinh JWT token.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Gọi hàm băm, kiểm tra mật khẩu và tạo JWT từ `app/core/security.py`.
- Tương tác với ORM Model `User` (`app/models/user.py`) và `Session` (`app/db/session.py`).
- Nhận dữ liệu input từ `app/schemas/user.py` (`UserCreate`, `UserUpdate`).
- Được gọi bởi các Router `app/api/routers/users.py`, `app/api/routers/auth.py` và Dependency `app/api/deps.py`.
"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, create_access_token, verify_password
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Tìm người dùng dựa theo username duy nhất.
    - Trả về đối tượng `User` nếu tìm thấy, hoặc `None` nếu không có.
    - SQL tương đương: SELECT * FROM users WHERE users.username = :username LIMIT 1;
    """
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)


def get_user(db: Session, user_id: int) -> User:
    """
    Tìm người dùng theo khóa chính `id`.
    - Nếu không tồn tại: Ném lỗi HTTP 404 Not Found.
    """
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def list_users(db: Session) -> list[User]:
    """
    Lấy danh sách tất cả người dùng trong hệ thống, sắp xếp theo ID tăng dần.
    """
    stmt = select(User).order_by(User.id)
    return list(db.scalars(stmt))


def create_user(db: Session, payload: UserCreate) -> User:
    """
    Tạo tài khoản người dùng mới:
    - B1: Kiểm tra xem username đã tồn tại chưa -> Nếu trùng ném lỗi 409 Conflict.
    - B2: Mã hóa mật khẩu plain text thành chuỗi băm bằng `hash_password()`.
    - B3: Lưu vào DB và trả về User vừa tạo.
    """
    if get_user_by_username(db, payload.username) is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    hashed_pwd = hash_password(payload.password)
    user = User(
        username=payload.username,
        hashed_password=hashed_pwd,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    """
    Cập nhật thông tin người dùng:
    - B1: Tìm user cần cập nhật theo ID.
    - B2: Kiểm tra nếu đổi username mới thì username đó đã bị ai khác chiếm chưa.
    - B3: Nếu có truyền password mới thì băm lại password; nếu không thì giữ nguyên password cũ.
    - B4: Lưu vào DB và trả về User.
    """
    user = get_user(db, user_id)

    # Kiểm tra xem username mới có bị trùng với một user KHÁC trong DB không
    existing_user = get_user_by_username(db, payload.username)
    if existing_user is not None and existing_user.id != user_id:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )
    
    user.username = payload.username
    user.role = payload.role
    # Chỉ cập nhật mật khẩu nếu người dùng truyền vào mật khẩu mới
    if payload.password is not None:
        user.hashed_password = hash_password(payload.password)
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    """
    Xóa tài khoản người dùng khỏi hệ thống theo ID.
    """
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()


def login(db: Session, username: str, password: str) -> str:
    """
    Xử lý logic Đăng nhập:
    - B1: Tìm user theo username trong DB.
    - B2: Nếu không thấy user HOẶC mật khẩu không khớp -> Ném lỗi 401 Unauthorized.
    (Dùng chung thông báo lỗi để tránh kẻ gian đoán biết được username nào đã tồn tại).
    - B3: Nếu hợp lệ -> Gọi `create_access_token` để tạo chuỗi JWT và trả về.
    """
    user = get_user_by_username(db, username)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    return create_access_token(user.username)
