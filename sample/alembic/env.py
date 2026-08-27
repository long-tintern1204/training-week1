"""
FILE: alembic/env.py
MỤC ĐÍCH:
- Cấu hình môi trường thực thi cho công cụ Database Migration (Alembic).
- Tự động nạp `DATABASE_URL` và `Base.metadata` từ code FastAPI để Alembic có thể so sánh
  giữa cấu trúc Model Python và cấu trúc bảng thực tế trong Database.

CÁCH DÙNG ALEMBIC:
- Sinh migration tự động: `alembic revision --autogenerate -m "tên_migration"`
- Chạy cập nhật database: `alembic upgrade head`
"""

from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db.database import DATABASE_URL, Base
from app.models import Book, User  # noqa: F401 - Import để metadata ghi nhận tất cả models

# Đọc file cấu hình alembic.ini
config = context.config

# Gán URL kết nối database lấy từ app/db/database.py (đồng bộ với FastAPI)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata chứa định nghĩa tất cả các bảng (Book, User...)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Chạy migration ở chế độ offline (sinh ra các câu lệnh SQL thuần mà không cần kết nối trực tiếp đến DB).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Chạy migration ở chế độ online (kết nối trực tiếp đến DB SQLite và thực thi cập nhật).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
