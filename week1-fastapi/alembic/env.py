"""
File: alembic/env.py
Mục đích: Cấu hình môi trường thực thi cho công cụ quản lý phiên bản cơ sở dữ liệu Alembic.

Liên kết với các file khác:
- app/database.py: Lấy `DATABASE_URL`, `Base`, và `engine` để Alembic biết kết nối tới đâu và theo dõi metadata nào.
- app/models: Nạp `Author` và `Book` để các model này được đăng ký vào `Base.metadata`.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Nạp thông tin kết nối và cấu trúc bảng từ mã nguồn ứng dụng
from app.database import DATABASE_URL, Base, engine
from app.models import Author, Book

# Đối tượng cấu hình của Alembic, đọc từ file alembic.ini
config = context.config

# Thiết lập hệ thống ghi log từ file cấu hình nếu có
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Gán metadata của các Model vào target_metadata:
# Nhờ dòng này, khi ta chạy `alembic revision --autogenerate`, Alembic sẽ tự động
# so sánh cấu trúc trong các class Model với Database thực tế để sinh script migration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Chạy migration ở chế độ 'offline' (không cần engine kết nối trực tiếp, chỉ sinh câu lệnh SQL)."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Chạy migration ở chế độ 'online' (kết nối trực tiếp đến Database và thực thi thay đổi)."""
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Kiểm tra chế độ chạy (Offline hay Online) để gọi hàm tương ứng
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
