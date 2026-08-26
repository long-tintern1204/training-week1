"""
File: app/models/__init__.py
Mục đích: Package index cho thư mục models. 
Gom nhóm và export các model `Author`, `Book` để các module khác (như `app/admin.py`, `main.py`, `alembic/env.py`)
có thể import ngắn gọn: `from app.models import Book, Author`.
"""

from app.models.author import Author
from app.models.book import Book

# __all__ khai báo danh sách các đối tượng được export công khai từ package này
__all__ = ["Book", "Author"]