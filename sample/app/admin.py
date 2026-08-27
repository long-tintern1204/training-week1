"""
FILE: app/admin.py
MỤC ĐÍCH:
- Cấu hình giao diện quản trị đồ họa (Admin Dashboard) bằng thư viện `sqladmin`.
- Giúp người quản trị có thể xem, thêm, sửa, xóa dữ liệu Book trực tiếp qua trình duyệt web tại `/admin`.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Nhận `Book` model từ `app/models/book.py`.
- Hàm `setup_admin()` được gọi trong `app/main.py` và nhận `app` cùng `engine` từ `app/db/session.py`.
"""

from sqladmin import Admin, ModelView

from app.models import Book


class BookAdmin(ModelView, model=Book):
    """
    Khai báo view quản trị cho bảng Book trên SQLAdmin:
    - column_list: Các cột hiển thị trên bảng danh sách.
    - name & name_plural: Nhãn hiển thị trên menu điều hướng.
    """
    column_list = [Book.id, Book.title, Book.year, Book.summary]
    name = "Book"
    name_plural = "Books"


def setup_admin(app, engine) -> Admin:
    """
    Khởi tạo và gắn Admin Dashboard vào ứng dụng FastAPI.
    - URL truy cập: http://127.0.0.1:8000/admin
    """
    admin = Admin(app, engine, title="Books Admin")
    admin.add_view(BookAdmin)
    return admin
