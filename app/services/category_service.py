from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Category, Book
from app.schemas.category import CategoryCreate, CategoryUpdate


def list_categories(db: Session) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    return list(db.scalars(stmt))


def get_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
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
    category = get_category(db, category_id)
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
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