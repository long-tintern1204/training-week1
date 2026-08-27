"""
FILE: app/schemas/book.py
MỤC ĐÍCH:
- Định nghĩa các Schema Pydantic cho dữ liệu Sách (Book Data Transfer Objects - DTO).
- Dùng để validate dữ liệu đầu vào từ client và serialize dữ liệu đầu ra từ server.

LIÊN KẾT VỚI CÁC FILE KHÁC:
- Dùng trong `app/services/book_service.py` để nhận payload tạo/cập nhật sách.
- Dùng trong `app/api/routers/books.py` để validate request body và định dạng response (`response_model=BookRead`).
"""

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """
    Schema kiểm tra dữ liệu khi Client gửi request tạo Sách mới (POST /books).
    - title: Độ dài từ 1 đến 200 ký tự.
    - year: Năm xuất bản phải từ năm 1000 đến 2100.
    - summary: Tóm tắt nội dung sách, tối đa 500 ký tự (không bắt buộc, mặc định None).
    """
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    summary: str | None = Field(default=None, max_length=500)


class BookUpdate(BaseModel):
    """
    Schema kiểm tra dữ liệu khi Client cập nhật Sách (PUT /books/{id}).
    """
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    summary: str | None = Field(default=None, max_length=500)


class BookRead(BaseModel):
    """
    Schema định dạng dữ liệu trả về cho Client (GET /books, GET /books/{id}, POST /books).
    - `from_attributes = True`: Cho phép Pydantic tự động đọc dữ liệu từ SQLAlchemy ORM Model (Book)
    và chuyển đổi thành JSON object trả về cho client.
    """
    id: int
    title: str
    year: int
    summary: str | None = None

    model_config = {"from_attributes": True}
