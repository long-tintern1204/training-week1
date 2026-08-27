"""
FILE: app/models/user.py
MỤC ĐÍCH:
- Khai báo ORM Model `User`, ánh xạ trực tiếp thành bảng `users` trong Database.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Kế thừa `Base` từ `app/db/database.py`.
- Được import bởi `app/models/__init__.py` để gom nhóm các model.
- Được sử dụng bởi `app/services/user_service.py` để thao tác dữ liệu người dùng (tạo tài khoản, kiểm tra đăng nhập).
- Được sử dụng bởi `app/api/deps.py` để trả về kiểu dữ liệu người dùng hiện tại (`current_user: User`).
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    """
    Bảng 'users' lưu thông tin người dùng:
    - id: Khóa chính (Primary Key), tự tăng.
    - username: Tên đăng nhập (duy nhất - unique, tối đa 50 ký tự, được đánh index để tìm nhanh).
    - hashed_password: Mật khẩu đã được mã hóa băm bằng bcrypt (không bao giờ lưu mật khẩu gốc).
    - role: Phân quyền tài khoản (0 = Admin có toàn quyền, 1 = Normal User thông thường). Mặc định là 1.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[int] = mapped_column(Integer, nullable=False, default=1)