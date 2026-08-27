# ==============================================================================
# TẬP TIN: app/admin.py
# VAI TRÒ: Cấu hình giao diện quản trị trực quan SQLAdmin Dashboard (URL: /admin)
# LIÊN KẾT:
#   - Nhận Models từ: app/models/__init__.py (Author, Book, Category)
#   - Được tích hợp vào FastAPI và Engine tại: app/main.py (setup_admin)
# ==============================================================================

from sqladmin import Admin, ModelView
from app.models import Author, Book, Category


class AuthorAdmin(ModelView, model=Author):
    """
    Cấu hình hiển thị bảng Tác giả (Author) trên trang Admin.
    """
    # Các cột hiển thị trong danh sách bảng
    column_list = [
        Author.id,
        Author.name,
        Author.bio,
        Author.country,
        Author.birth_year,
    ]
    name = "Author"
    name_plural = "Authors"
    

class BookAdmin(ModelView, model=Book):
    """
    Cấu hình hiển thị bảng Sách (Book) trên trang Admin.
    """
    column_list = [
        Book.id,
        Book.title,
        Book.author_id,
        Book.category_id,
        Book.summary,
        Book.year,
    ]
    name = "Book"
    name_plural = "Books"
    

class CategoryAdmin(ModelView, model=Category):
    """
    Cấu hình hiển thị bảng Thể loại (Category) trên trang Admin.
    """
    column_list = [Category.id, Category.name]
    name = "Category"
    name_plural = "Categories"


def setup_admin(app, engine) -> Admin:
    """
    Khởi tạo và đăng ký giao diện SQLAdmin vào ứng dụng FastAPI:
    - Tạo đối tượng Admin gắn với FastAPI app và SQLAlchemy engine.
    - Đăng ký các ModelView quản trị cho Author, Book, Category.
    - Truy cập trang quản trị tại: http://127.0.0.1:8000/admin
    """
    admin = Admin(app, engine, title="Books Admin")
    admin.add_view(AuthorAdmin)
    admin.add_view(BookAdmin)
    admin.add_view(CategoryAdmin)
    return admin
