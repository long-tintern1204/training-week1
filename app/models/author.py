from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    bio: Mapped[str] = mapped_column(String(1000), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=True)
