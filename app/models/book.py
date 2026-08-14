from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=True)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("authors.id"), nullable=True)
    author = relationship("Author", back_populates="books")
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="books")