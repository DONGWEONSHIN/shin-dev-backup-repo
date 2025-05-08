"""LangGraph RAG 서버의 FastAPI 엔트리포인트입니다."""

from contextlib import asynccontextmanager

from app.api.v1 import rag
from app.core.config import (
    STATIC_DIR,
    TEMPLATES_DIR,
    clear_directories,
    ensure_directories,
)
from app.web import views
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


@asynccontextmanager
async def lifespan(_: FastAPI):
    """앱 시작 시 필요한 폴더를 생성합니다."""
    clear_directories()
    ensure_directories()
    yield


# FastAPI 앱 생성
app = FastAPI(title="LangGraph RAG Server", lifespan=lifespan)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 및 템플릿 디렉토리 설정
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# 라우터 등록
app.include_router(rag.router, prefix="/api/v1/rag")
app.include_router(views.router)
