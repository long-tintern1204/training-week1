# ==============================================================================
# TẬP TIN: app/schemas/author.py
# VAI TRÒ: Định nghĩa các Pydantic Schemas cho Tác giả (Data Transfer Objects - DTO)
# LIÊN KẾT:
#   - Dùng để validate dữ liệu đầu vào cho Router: app/api/routers/authors.py
#   - Dùng làm kiểu dữ liệu tham số và trả về trong: app/services/author_service.py
# ==============================================================================

from pydantic import BaseModel, Field


class AuthorCreate(BaseModel):
    """
    Schema nhận dữ liệu khi tạo mới một Tác giả (POST /api/v1/authors).
    FastAPI sẽ tự động kiểm tra tính hợp lệ của dữ liệu dựa trên các ràng buộc dưới đây:
    """
    # Tên bắt buộc, độ dài từ 1 đến 200 ký tự
    name: str = Field(min_length=1, max_length=200)
    # Tiểu sử tùy chọn, tối đa 1000 ký tự
    bio: str | None = Field(default=None, max_length=1000)
    # Quốc gia tùy chọn, tối đa 100 ký tự
    country: str | None = Field(default=None, max_length=100)
    # Năm sinh tùy chọn, phải nằm trong khoảng từ năm 1000 đến 2100 (ge: >=, le: <=)
    birth_year: int | None = Field(default=None, ge=1000, le=2100)


class AuthorUpdate(BaseModel):
    """
    Schema nhận dữ liệu khi cập nhật thông tin Tác giả (PUT /api/v1/authors/{id}).
    """
    name: str = Field(min_length=1, max_length=200)
    bio: str | None = Field(default=None, max_length=1000)
    country: str | None = Field(default=None, max_length=100)
    birth_year: int | None = Field(default=None, ge=1000, le=2100)
    

class AuthorRead(BaseModel):
    """
    Schema định dạng dữ liệu Tác giả trả về cho Client (GET /api/v1/authors/...).
    """
    id: int
    name: str 
    bio: str | None = None
    country: str | None = None
    birth_year: int | None = None

    # from_attributes = True (trước đây là orm_mode = True trong Pydantic v1)
    # Cho phép Pydantic tự động đọc dữ liệu từ các thuộc tính của đối tượng ORM Model (SQLAlchemy Author)
    model_config = {"from_attributes": True}
