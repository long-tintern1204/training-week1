"""
FILE: app/core/security.py
MỤC ĐÍCH:
- Chứa các hàm tiện ích liên quan đến BẢO MẬT:
  1. Băm mật khẩu (Hash password) bằng thuật toán `bcrypt`.
  2. Xác thực mật khẩu khi đăng nhập (Verify password).
  3. Tạo chuỗi mã hóa JSON Web Token (JWT Access Token).

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Lấy cấu hình (`secret_key`, `jwt_algorithm`, `access_token_expire_minutes`) từ `app/core/config.py`.
- Được gọi bởi `app/services/user_service.py` khi tạo user, cập nhật mật khẩu và khi user đăng nhập.
- Chuỗi JWT tạo ra ở đây sẽ được giải mã và kiểm tra tại `app/api/deps.py`.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings


def hash_password(plain: str) -> str:
    """
    Băm mật khẩu người dùng dạng plain text thành chuỗi mã hóa an toàn.
    Sử dụng bcrypt với muối ngẫu nhiên (salt).
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Kiểm tra mật khẩu người dùng nhập vào (plain) có khớp với chuỗi đã băm trong DB (hashed) hay không.
    Trả về True nếu đúng, False nếu sai.
    """
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(subject: str) -> str:
    """
    Tạo chuỗi JWT Access Token chứa thông tin định danh (thường là username).
    - `subject` (sub): username của người dùng.
    - `exp`: thời điểm token hết hạn (tính theo giờ UTC hiện tại + số phút cấu hình).
    """
    settings = get_settings()
    # Tính thời gian hết hạn theo chuẩn UTC
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    # Dữ liệu payload nhúng vào bên trong token
    payload = {
        "sub": subject,
        "exp": expire,
    }
    # Ký và mã hóa token bằng secret_key
    encoded_jwt = jwt.encode(
        payload, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt