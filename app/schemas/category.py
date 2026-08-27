# ==============================================================================
# TẬP TIN: app/schemas/category.py
# VAI TRÒ: Định nghĩa các Pydantic Schemas cho Thể loại/Danh mục sách (DTO)
# LIÊN KẾT:
#   - Dùng để validate dữ liệu đầu vào cho Router: app/api/routers/categories.py
#   - Dùng làm kiểu dữ liệu tham số và trả về trong: app/services/category_service.py
# ==============================================================================

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """
    Schema nhận dữ liệu khi tạo mới Danh mục (POST /api/v1/categories).
    """
    name: str = Field(min_length=1, max_length=100)


class CategoryUpdate(BaseModel):
    """
    Schema nhận dữ liệu khi cập nhật Danh mục (PUT /api/v1/categories/{id}).
    """
    name: str = Field(min_length=1, max_length=100)


class CategoryRead(BaseModel):
    """
    Schema định dạng dữ liệu Danh mục trả về cho Client (GET /api/v1/categories/...).
    """
    id: int
    name: str
    
    # Cho phép Pydantic tự động đọc dữ liệu từ SQLAlchemy Category ORM model
    model_config = {"from_attributes": True}