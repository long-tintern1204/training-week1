# Books API — Sample

Copy toàn bộ nội dung folder này vào nhánh `week2/fastapi-crud-validation`, rồi:

```bash
python -m venv venv
# activate venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin
- http://127.0.0.1:8000/docs


├── README.md                 : Tài liệu hướng dẫn dự án (giới thiệu, cách cài đặt, cách chạy code)
├── alembic                   : Thư mục chứa công cụ quản lý sự thay đổi cấu trúc database (Migrations)
│   ├── env.py                : Tệp cấu hình môi trường để kết nối mã nguồn với công cụ Alembic
│   ├── script.py.mako        : Khuôn mẫu (Template) để Alembic sinh ra các file cập nhật database tự động
│   └── versions              : Nơi chứa các file lịch sử ghi lại việc thêm, sửa, xóa các bảng/cột
├── alembic.ini               : Tệp cấu hình gốc của Alembic
├── app                       : Thư mục chứa toàn bộ bộ não và mã nguồn chính của ứng dụng
│   ├── __init__.py           : (File trống) Báo cho Python biết thư mục này là một module
│   ├── admin.py              : Cấu hình giao diện quản trị viên (Admin Dashboard)
│   ├── api                   : Tầng giao tiếp, nơi trực tiếp nhận các yêu cầu (Request) từ bên ngoài
│   │   ├── __init__.py       : (File trống)
│   │   └── routers           : Nơi định nghĩa các đường dẫn API cụ thể (ví dụ: GET /books, POST /books)
│   │       └── __init__.py   : (File trống)
│   ├── core                  : Tầng chứa các thành phần cốt lõi của toàn hệ thống
│   │   ├── __init__.py       : (File trống)
│   │   └── config.py         : Trung tâm quản lý cài đặt (đọc file .env, cấu hình bảo mật)
│   ├── db                    : Tầng quản lý kết nối cơ sở dữ liệu
│   │   ├── __init__.py       : (File trống)
│   │   ├── database.py       : Nền tảng thiết lập cơ sở dữ liệu (nơi chuẩn bị địa chỉ và nền móng)
│   │   └── session.py        : Tạo và quản lý các phiên làm việc (sessions) kết nối đến DB
│   ├── main.py               : Điểm neo khởi chạy ứng dụng (nơi khởi tạo FastAPI và nhúng các routers)
│   ├── models                : Nơi định nghĩa các bảng dữ liệu sẽ lưu vào database (SQLAlchemy ORM)
│   │   └── __init__.py       : (File trống)
│   ├── schemas               : Nơi xác thực, kiểm tra lỗi định dạng dữ liệu đầu vào và đầu ra (Pydantic)
│   │   └── __init__.py       : (File trống)
│   └── services              : Tầng nghiệp vụ (chứa các đoạn code xử lý logic tinh toán phức tạp)
│       └── __init__.py       : (File trống)
├── data                      : Thư mục chứa các tệp dữ liệu vật lý (cục bộ)
│   └── books.db              : Tệp cơ sở dữ liệu SQLite chứa dữ liệu thực tế của ứng dụng
└── requirements.txt          : Danh sách các thư viện cần cài đặt để chạy dự án (pip install -r ...)