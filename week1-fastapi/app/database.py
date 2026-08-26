"""
File: app/database.py
Mục đích: Thiết lập kết nối cơ sở dữ liệu SQLite và cung cấp Session làm việc cho toàn bộ ứng dụng.

Liên kết với các file khác:
- app/models/author.py & app/models/book.py: Kế thừa lớp `Base` từ file này để định nghĩa bảng.
- app/admin.py & alembic/env.py: Sử dụng `engine` và `DATABASE_URL` từ file này để kết nối DB.
- main.py: Sử dụng `get_db` làm Dependency để cung cấp session DB cho các API endpoint.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Xác định đường dẫn thư mục lưu file cơ sở dữ liệu SQLite (thư mục data/)
# Path(__file__).resolve().parent.parent: Đi từ 'app/database.py' lên thư mục gốc 'week1-fastapi'
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
# Tự động tạo thư mục 'data' nếu thư mục này chưa tồn tại
DATA_DIR.mkdir(exist_ok=True)

# 2. Chuỗi kết nối Database (Database URL) trỏ tới file SQLite 'books.db' trong thư mục 'data'
DATABASE_URL = f"sqlite:///{DATA_DIR / 'books.db'}"

# 3. Khởi tạo SQLAlchemy Engine: Cầu nối quản lý các kết nối vật lý đến file SQLite
# check_same_thread=False: Bắt buộc đối với SQLite khi chạy với FastAPI để cho phép nhiều thread cùng truy cập
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# 4. Tạo factory SessionLocal: Dùng để sinh ra các phiên làm việc (Session) với database
# autocommit=False: Không tự động commit, ta phải gọi db.commit() một cách chủ động
# autoflush=False: Không tự động đẩy thay đổi xuống DB trước mỗi câu query trừ khi cần
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 5. Lớp Base kế thừa DeclarativeBase:
# Tất cả các ORM Models (Author, Book) sau này sẽ kế thừa từ Base này để SQLAlchemy quản lý Metadata các bảng
class Base(DeclarativeBase):
    pass


# 6. Dependency `get_db`: Cung cấp Session DB cho từng Request trong FastAPI
# Cơ chế hoạt động:
# - Khi có request gọi vào router có `Depends(get_db)`, một session mới (`db`) được mở ra.
# - Lệnh `yield db` tạm dừng hàm và trả `db` cho router sử dụng.
# - Sau khi router xử lý xong (kể cả có lỗi hay không), khối `finally` sẽ chạy `db.close()` để đóng kết nối, giải phóng tài nguyên.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
