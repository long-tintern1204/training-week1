"""
FILE: app/schemas/user.py
MỤC ĐÍCH:
- Định nghĩa các Schema Pydantic cho dữ liệu Người dùng và Xác thực (Authentication).
- Đảm bảo mật khẩu người dùng không bao giờ bị trả về cho client thông qua schema `UserRead`.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Dùng trong `app/services/user_service.py` để nhận payload tạo/cập nhật user.
- Dùng trong `app/api/routers/users.py` và `app/api/routers/auth.py` để validate và format response.
"""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """
    Schema nhận dữ liệu đăng ký/tạo User mới (POST /users).
    - username: Tối thiểu 3, tối đa 50 ký tự.
    - password: Mật khẩu dạng thô (plain text), tối thiểu 8 ký tự để đảm bảo an toàn.
    - role: Phân quyền (0 = Admin, 1 = Normal User), mặc định là 1.
    """
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)
    role: int = 1


class UserRead(BaseModel):
    """
    Schema định dạng thông tin User trả về cho Client (GET /users, GET /users/{id}, GET /auth/me).
    LƯU Ý QUAN TRỌNG: Schema này TUYỆT ĐỐI KHÔNG chứa trường `password` hay `hashed_password`
    để đảm bảo tính bảo mật.
    """
    id: int
    username: str
    role: int

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """
    Schema nhận dữ liệu cập nhật User (PUT /users/{id}).
    - password: Có thể cập nhật (nếu nhập tối thiểu 8 ký tự) hoặc để trống (None) nếu không muốn đổi pass.
    """
    username: str = Field(min_length=3, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=100)
    role: int = 1


class LoginRequest(BaseModel):
    """
    Schema nhận dữ liệu khi người dùng đăng nhập (POST /auth/login).
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Schema trả về JWT Access Token sau khi đăng nhập thành công.
    - access_token: Chuỗi mã hóa JWT.
    - token_type: Loại token (chuẩn là 'bearer').
    """
    access_token: str
    token_type: str = "bearer"