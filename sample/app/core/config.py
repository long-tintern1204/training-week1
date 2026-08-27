"""
FILE: app/core/config.py
MỤC ĐÍCH:
- Quản lý tất cả các cấu hình (Settings) và biến môi trường của dự án.
- Sử dụng thư viện `pydantic-settings` để tự động đọc và validate file `.env`.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Được import bởi `app/core/security.py`: lấy `secret_key`, `jwt_algorithm`, `access_token_expire_minutes`.
- Được import bởi `app/db/database.py`: lấy `database_url`.
- Được import bởi `app/main.py`: lấy `app_title`.
- Được import bởi `app/api/deps.py`: lấy `secret_key` để giải mã token.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Lớp cấu hình ứng dụng kế thừa từ BaseSettings của Pydantic.
    Tự động map các biến trong file `.env` vào các thuộc tính bên dưới:
    """
    app_title: str = "Books API"                     # Tên ứng dụng hiển thị trên Swagger UI
    database_url: str | None = None                  # URL kết nối DB (nếu None sẽ dùng SQLite mặc định)
    secret_key: str                                  # Khóa bí mật để ký JWT token (BẮT BUỘC có trong .env)
    jwt_algorithm: str = "HS256"                     # Thuật toán mã hóa JWT (mặc định HS256)
    access_token_expire_minutes: int = 30            # Thời gian sống của Access Token (phút)

    # Cấu hình đọc từ file .env, bỏ qua các biến thừa không khai báo trong class
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """
    Hàm lấy instance cấu hình (Singleton Pattern bằng @lru_cache).
    @lru_cache giúp lưu cache kết quả, chỉ đọc file .env một lần duy nhất lúc khởi động,
    tránh việc đọc đĩa nhiều lần gây giảm hiệu năng.
    """
    return Settings()
