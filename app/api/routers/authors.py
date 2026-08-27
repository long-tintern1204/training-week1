# ==============================================================================
# TẬP TIN: app/api/routers/authors.py
# VAI TRÒ: Tầng tiếp nhận HTTP Request và trả về Response cho Tác giả (Authors API)
# ĐƯỜNG DẪN GỐC: /api/v1/authors (do app/main.py gắn prefix /api/v1)
# LIÊN KẾT:
#   - Nhận DB Session từ: app/db/session.py (get_db)
#   - Validate dữ liệu với: app/schemas/author.py (AuthorCreate, AuthorRead, AuthorUpdate)
#   - Chuyển giao logic cho: app/services/author_service.py
# ==============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.services import author_service

# Khởi tạo Router riêng cho Authors, gom nhóm tag "authors" trong Swagger Docs
router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", response_model=list[AuthorRead])
def list_authors(db: Session = Depends(get_db)) -> list[AuthorRead]:
    """
    [GET] /api/v1/authors/
    Lấy danh sách tất cả các tác giả.
    """
    return author_service.list_authors(db)


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)) -> AuthorRead:
    """
    [GET] /api/v1/authors/{author_id}
    Lấy thông tin chi tiết một tác giả theo ID từ URL Path.
    """
    return author_service.get_author(db, author_id)


@router.post("/", response_model=AuthorRead, status_code=201)
def create_author(
    payload: AuthorCreate,
    db: Session = Depends(get_db),
) -> AuthorRead:
    """
    [POST] /api/v1/authors/
    Tạo mới một tác giả.
    - payload: Nhận JSON Body và tự động validate bằng AuthorCreate schema.
    - status_code=201: Chuẩn HTTP Created.
    """
    return author_service.create_author(db, payload)


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int,
    payload: AuthorUpdate,
    db: Session = Depends(get_db),
) -> AuthorRead:
    """
    [PUT] /api/v1/authors/{author_id}
    Cập nhật thông tin tác giả theo ID.
    """
    return author_service.update_author(db, author_id, payload)


@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)) -> None:
    """
    [DELETE] /api/v1/authors/{author_id}
    Xóa một tác giả theo ID.
    - status_code=204: Chuẩn HTTP No Content (xóa thành công không cần trả về body).
    """
    return author_service.delete_author(db, author_id)