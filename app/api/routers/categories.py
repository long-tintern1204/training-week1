# ==============================================================================
# TẬP TIN: app/api/routers/categories.py
# VAI TRÒ: Tầng tiếp nhận HTTP Request và trả về Response cho Thể loại (Categories API)
# ĐƯỜNG DẪN GỐC: /api/v1/categories (do app/main.py gắn prefix /api/v1)
# LIÊN KẾT:
#   - Nhận DB Session từ: app/db/session.py (get_db)
#   - Validate dữ liệu với: app/schemas/category.py (CategoryCreate, CategoryRead, CategoryUpdate)
#   - Chuyển giao logic cho: app/services/category_service.py
# ==============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services import category_service

# Khởi tạo Router riêng cho Categories, gom nhóm tag "categories" trong Swagger Docs
router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:
    """
    [GET] /api/v1/categories/
    Lấy danh sách tất cả các thể loại/danh mục.
    """
    return category_service.list_categories(db)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryRead:
    """
    [GET] /api/v1/categories/{category_id}
    Lấy thông tin chi tiết một danh mục theo ID từ URL Path.
    """
    return category_service.get_category(db, category_id)


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryRead:
    """
    [POST] /api/v1/categories/
    Tạo mới một danh mục.
    """
    return category_service.create_category(db, payload)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
) -> CategoryRead:
    """
    [PUT] /api/v1/categories/{category_id}
    Cập nhật tên danh mục theo ID.
    """
    return category_service.update_category(db, category_id, payload)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> None:
    """
    [DELETE] /api/v1/categories/{category_id}
    Xóa một danh mục theo ID.
    """
    return category_service.delete_category(db, category_id)