"""
File: app/admin.py
Mục đích: Cấu hình giao diện Admin trực quan (Dashboard) cho ứng dụng bằng thư viện `sqladmin`.

Liên kết với các file khác:
- app/models: Import `Author` và `Book` để tạo view quản trị tương ứng cho 2 bảng.
- app/database.py: Nhận đối tượng `engine` truyền vào từ `main.py` để kết nối CSDL.
- main.py: Gọi hàm `setup_admin(app, engine)` sau khi khởi tạo FastAPI để kích hoạt đường dẫn `/admin`.
"""

from sqladmin import Admin, ModelView

from app.models import Book, Author


# 1. Định nghĩa View quản trị cho bảng Author (Tác giả)
class AuthorAdmin(ModelView, model=Author):
    column_list = [Author.id, Author.name]

    # Tìm kiếm và sắp xếp
    column_searchable_list = [Author.name]
    column_sortable_list = [Author.id, Author.name]

    # Tên hiển thị trên menu
    name = "Author"
    name_plural = "Authors"
    icon = "fa-solid fa-user"  # Icon tùy chọn (FontAwesome)


# 2. Định nghĩa View quản trị cho bảng Book (Sách)
class BookAdmin(ModelView, model=Book):
    # Hiển thị Book.author nếu có relationship, hoặc giữ Book.author_id nếu chưa setup relationship
    column_list = [Book.id, Book.title, Book.author, Book.year]

    # Các cột chỉ hiển thị khi bấm vào xem chi tiết (tránh làm bảng danh sách bị quá dài)
    column_details_list = [
        Book.id,
        Book.title,
        Book.author,
        Book.year,
        Book.summary,
    ]

    # Tìm kiếm theo tên sách
    column_searchable_list = [Book.title]
    column_sortable_list = [Book.id, Book.year]

    # Tên hiển thị chuẩn số ít / số nhiều
    name = "Book"
    name_plural = "Books"
    icon = "fa-solid fa-book"  # Icon tùy chọn


# 3. Hàm khởi tạo và gắn Admin Dashboard vào ứng dụng FastAPI
def setup_admin(app, engine):
    """
    Khởi tạo trang Admin tại đường dẫn `/admin` và đăng ký các ModelView quản trị.
    - app: Instance FastAPI được tạo từ `main.py`
    - engine: SQLAlchemy engine tạo từ `app/database.py`
    """
    admin = Admin(app, engine, title="Books Admin")
    # Đăng ký các view quản lý vào trang admin
    admin.add_view(BookAdmin)
    admin.add_view(AuthorAdmin)
    return admin
