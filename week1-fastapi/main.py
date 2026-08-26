"""
File: main.py
Mục đích: Entry point (Điểm khởi chạy chính) của ứng dụng FastAPI.
File này chịu trách nhiệm:
1. Khởi tạo ứng dụng FastAPI.
2. Gắn kết giao diện Admin (`setup_admin`).
3. Định nghĩa các Pydantic Schemas để validate dữ liệu đầu vào.
4. Định nghĩa các API endpoints (Router / Controller) để xử lý các yêu cầu CRUD sách.

Liên kết với các file khác:
- app/database.py: Nhận `engine` để cấu hình admin, nhận `get_db` để inject Session kết nối CSDL vào API.
- app/models: Nhận `Book` và `Author` để truy vấn và thao tác dữ liệu qua SQLAlchemy ORM.
- app/admin.py: Gọi `setup_admin(app, engine)` để kích hoạt trang quản trị tại `/admin`.
"""

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import các thành phần từ tầng cơ sở dữ liệu và models
from app.database import Base, engine, get_db
from app.models import Book, Author
from app.admin import setup_admin

# ==========================================
# 1. KHỞI TẠO FASTAPI APP & ADMIN
# ==========================================
app = FastAPI(title="Books API")

# (Ghi chú: Lệnh Base.metadata.create_all(bind=engine) bị comment vì dự án quản lý bảng qua Alembic migration)
# Base.metadata.create_all(bind=engine)

# Kích hoạt giao diện Admin Dashboard tại đường dẫn '/admin'
setup_admin(app, engine)


# ==========================================
# 2. PYDANTIC SCHEMAS (DATA VALIDATION)
# ==========================================
# Schema dùng để validate dữ liệu khi tạo Tác giả (Author)
class AuthorCreate(BaseModel):
    name: str  # Tên tác giả bắt buộc phải là kiểu chuỗi (string)


# Schema dùng để validate dữ liệu khi Tạo mới hoặc Cập nhật Sách (Book)
class BookCreate(BaseModel):
    title: str                  # Tiêu đề sách (bắt buộc)
    year: int                   # Năm xuất bản (bắt buộc, kiểu số nguyên)
    summary: str | None = None  # Tóm tắt nội dung (tuỳ chọn, mặc định None)
    author_id: int | None = None  # ID tác giả (tuỳ chọn, mặc định None)


# ==========================================
# 3. API ENDPOINTS (ROUTES / CONTROLLER LOGIC)
# ==========================================

# ------------------------------------------
# GET /: Endpoint kiểm tra trạng thái API
# ------------------------------------------
@app.get("/")
def root():
    """Kiểm tra server đang hoạt động."""
    return {"message": "HELLO WORLD"}


# ------------------------------------------
# GET /books: Lấy danh sách tất cả các cuốn sách
# ------------------------------------------
@app.get("/books")
def list_books(db: Session = Depends(get_db)):
    """
    Lấy toàn bộ danh sách sách trong database.
    - db: Session được FastAPI tự động inject thông qua Depends(get_db)
    - db.query(Book).all(): Thực hiện câu lệnh SQL 'SELECT * FROM books'
    """
    return db.query(Book).all()


# ------------------------------------------
# GET /books/{book_id}: Lấy thông tin chi tiết một cuốn sách theo ID
# ------------------------------------------
@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Tìm kiếm sách theo ID.
    - db.get(Book, book_id): Tìm bản ghi Book có khóa chính là book_id
    - Nếu không tìm thấy, ném ra lỗi 404 Not Found
    """
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ------------------------------------------
# POST /books: Tạo mới một cuốn sách
# ------------------------------------------
@app.post("/books", status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    """
    Tạo mới một cuốn sách.
    - payload: Dữ liệu JSON từ client gửi lên, được Pydantic tự động parse và validate theo `BookCreate`.
    - Logic kiểm tra: Nếu client truyền `author_id`, ta kiểm tra xem tác giả đó có tồn tại trong CSDL không.
      Nếu không tồn tại -> Báo lỗi 404 "Author not found".
    - Book(**payload.model_dump()): Chuyển dữ liệu từ schema sang SQLAlchemy Model.
    - db.add() -> db.commit() -> db.refresh(): Lưu bản ghi vào SQLite và lấy lại dữ liệu mới nhất (gồm ID tự sinh).
    """
    # 1. Kiểm tra tác giả (nếu có truyền author_id)
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
            
    # 2. Tạo đối tượng model Book từ dữ liệu payload
    book = Book(**payload.model_dump())
    
    # 3. Lưu vào Database
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return book


# ------------------------------------------
# PUT /books/{book_id}: Cập nhật thông tin sách
# ------------------------------------------
@app.put("/books/{book_id}")
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    """
    Cập nhật toàn bộ thông tin của một cuốn sách theo ID.
    - 1. Kiểm tra xem cuốn sách cần sửa có tồn tại không.
    - 2. Nếu có cập nhật `author_id`, kiểm tra xem tác giả mới có tồn tại trong CSDL không.
    - 3. Dùng vòng lặp cập nhật từng thuộc tính từ payload vào model `book`.
    - 4. Lưu lại vào DB và trả về đối tượng đã cập nhật.
    """
    # 1. Tìm cuốn sách cần sửa
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # 2. Kiểm tra tính hợp lệ của author_id mới
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
            
    # 3. Gán các giá trị mới từ payload vào model instance
    for key, value in payload.model_dump().items():
        setattr(book, key, value)
        
    # 4. Commit thay đổi xuống SQLite
    db.commit()
    db.refresh(book)
    
    return book


# ------------------------------------------
# DELETE /books/{book_id}: Xóa một cuốn sách
# ------------------------------------------
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Xóa một cuốn sách theo ID.
    - Trả về status_code=204 (No Content) khi xóa thành công.
    - Nếu không tìm thấy sách để xóa -> Báo lỗi 404.
    """
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # Thực hiện câu lệnh DELETE trong SQL
    db.delete(book)
    db.commit()
    
    return None
