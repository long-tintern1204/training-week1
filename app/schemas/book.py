# ==============================================================================
# TẬP TIN: app/schemas/book.py
# VAI TRÒ: Định nghĩa các Pydantic Schemas cho Sách (Data Transfer Objects - DTO)
# LIÊN KẾT:
#   - Dùng để validate dữ liệu đầu vào cho Router: app/api/routers/books.py
#   - Dùng làm kiểu dữ liệu tham số và trả về trong: app/services/book_service.py
# ==============================================================================

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """
    Schema nhận dữ liệu khi tạo mới Sách (POST /api/v1/books).
    """
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    summary: str | None = Field(default=None, max_length=500)
    author_id: int | None = None
    category_id: int | None = None
    

class BookUpdate(BaseModel):
    """
    Schema nhận dữ liệu khi cập nhật thông tin Sách (PUT /api/v1/books/{id}).
    """
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1000, le=2100)
    summary: str | None = Field(default=None, max_length=500)
    author_id: int | None = None
    category_id: int | None = None
    
    
class BookRead(BaseModel):
    """
    Schema định dạng dữ liệu Sách trả về cho Client (GET /api/v1/books/...).
    Đặc biệt: Chứa cả author_name và category_name để Client không cần gọi thêm API khác để lấy tên.
    """
    id: int
    title: str
    year: int
    summary: str | None = None
    author_id: int | None = None
    author_name: str | None = None
    category_id: int | None = None
    category_name: str | None = None