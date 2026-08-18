from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.admin import setup_admin
from app.api.routers import books
from app.core.config import get_settings
from app.db.database import Base
from app.db.session import engine
from app.models import Book  # noqa: F401

settings = get_settings()
app = FastAPI(title=settings.app_title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # TODO: origin Vite `npm run dev` — localhost
        # TODO: origin Vite `npm run dev` — 127.0.0.1
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
setup_admin(app, engine)

app.include_router(books.router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World"}
