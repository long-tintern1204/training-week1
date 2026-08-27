# ==============================================================================
# TẬP TIN: app/services/category_service.py
# VAI TRÒ: Tầng xử lý logic nghiệp vụ và truy vấn CSDL cho Danh mục (Categories)
# LIÊN KẾT:
#   - Được gọi bởi Router: app/api/routers/categories.py
#   - Sử dụng Models: app/models/category.py (Category), app/models/book.py (Book)
#   - Sử dụng Schemas: app/schemas/category.py (CategoryCreate, CategoryUpdate)
# ==============================================================================

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Category, Book
from app.schemas.category import CategoryCreate, CategoryUpdate


def list_categories(db: Session) -> list[Category]:
    """
    Lấy danh sách tất cả danh mục trong CSDL, sắp xếp tăng dần theo ID.
    """
    stmt = select(Category).order_by(Category.id)
    return list(db.scalars(stmt))


def get_category(db: Session, category_id: int) -> Category:
    """
    Lấy thông tin chi tiết một danh mục theo ID.
    Văng lỗi HTTP 404 (Not Found) nếu không tìm thấy.
    """
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    """
    Tạo mới một danh mục.
    """
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    db: Session,
    category_id: int,
    payload: CategoryUpdate,
) -> Category:
    """
    Cập nhật tên danh mục theo ID.
    """
    category = get_category(db, category_id)
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    """
    Xóa một danh mục theo ID.
    LOGIC NGHIỆP VỤ ĐẶC BIỆT:
    - Trước khi xóa, đếm xem danh mục này có đang chứa cuốn sách nào không.
    - Nếu số lượng sách > 0: Văng lỗi HTTP 409 (Conflict), chặn không cho xóa.
    - Nếu không có sách: Xóa bản ghi danh mục.
    """
    category = get_category(db, category_id)
    stmt = select(func.count(Book.id)).where(Book.category_id == category_id)
    book_count = db.scalar(stmt)
    if book_count > 0:
        raise HTTPException(
            status_code=409, 
            detail="Cannot delete category while books exist"
        )
    db.delete(category)
    db.commit()