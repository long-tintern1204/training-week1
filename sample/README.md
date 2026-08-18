# Books API — Sample tuần 3

Copy hết file trong folder này vào nhánh `week3/fastapi-jwt-auth`.

```bash
python -m venv venv
# Git Bash: source venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/admin

Sample có CRUD Book. GET không cần đăng nhập. Tuần này làm: CRUD User, login JWT, gắn token khi ghi sách, chỉ admin được xóa; rồi điền CORS 5173 và clone front-end (`npm run dev`).

CORS trong `app/main.py` đang là TODO. Front-end: https://github.com/Phongnx-vnext/intern202607_week3_frontend
