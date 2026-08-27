# ==============================================================================
# TẬP TIN: app/core/config.py
# VAI TRÒ: Quản lý cấu hình toàn ứng dụng (Settings & Environment Variables)
# LIÊN KẾT:
#   - Được gọi bởi app/db/database.py (lấy database_url)
#   - Được gọi bởi app/main.py (lấy app_title)
# ==============================================================================

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Class quản lý cấu hình hệ thống kế thừa từ BaseSettings của Pydantic.
    Tự động đọc các giá trị cấu hình từ biến môi trường hoặc file .env nếu có.
    """
    # Tên tiêu đề của ứng dụng API (mặc định là "Books API")
    app_title: str = "Books API"
    
    # Đường dẫn kết nối CSDL (nếu để None thì app/db/database.py sẽ dùng SQLite mặc định)
    database_url: str | None = None

    # Thiết lập đọc từ file .env, bỏ qua các biến thừa không khai báo trong class
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """
    Hàm lấy instance của Settings.
    Sử dụng decorator @lru_cache để chỉ khởi tạo Settings một lần duy nhất (Singleton Pattern),
    giúp tối ưu hiệu năng và tránh việc đọc lại file cấu hình nhiều lần.
    """
    return Settings()
