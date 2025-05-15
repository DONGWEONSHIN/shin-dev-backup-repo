"""웹 라우터 및 PDF 업로드/삭제 뷰를 제공하는 모듈입니다."""

import os
from datetime import timedelta
from typing import Optional

from app.core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_new_user,
    get_current_user,
)
from app.core.config import (
    CHROMA_PERSIST_DIR,
    DOCUMENTS_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_EMBEDDING_MODEL,
    TEMPLATES_DIR,
)
from app.core.document_ingest import ingest_documents
from app.core.models import User
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


async def get_current_user_or_none(request: Request) -> Optional[User]:
    """현재 사용자를 반환하거나 없으면 None을 반환합니다."""
    try:
        token = request.cookies.get("access_token")
        if not token:
            return None
        user = await get_current_user(token)
        return user
    except Exception:  # 일반적인 예외 처리로 변경
        return None


async def get_current_user_from_cookie(request: Request) -> User:
    """쿠키 또는 헤더에서 현재 사용자를 가져옵니다."""
    # 헤더에서 토큰 확인
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        try:
            user = await get_current_user(token)
            return user
        except Exception:
            # 헤더 토큰이 실패하면 쿠키 확인
            pass

    # 쿠키에서 토큰 확인
    user = await get_current_user_or_none(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 인덱스 페이지(HTML)를 렌더링합니다."""
    user = await get_current_user_or_none(request)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """로그인 페이지를 렌더링합니다."""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """로그인을 처리합니다."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "이메일 또는 비밀번호가 올바르지 않습니다.",
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """회원가입 페이지를 렌더링합니다."""
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
):
    """회원가입을 처리합니다."""
    if password != password2:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "비밀번호가 일치하지 않습니다."},
        )
    try:
        create_new_user(email, password)  # 반환값은 사용하지 않음
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": e.detail}
        )


@router.post("/logout")
async def logout():
    """로그아웃을 처리합니다."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response


@router.get("/pdf_list")
async def pdf_list(request: Request):
    """업로드된 PDF 파일 목록을 반환합니다."""
    current_user = await get_current_user_from_cookie(request)

    user_dir = os.path.join(DOCUMENTS_DIR, current_user.id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    pdfs = [f for f in os.listdir(user_dir) if f.lower().endswith(".pdf")]
    return {"pdfs": pdfs}


@router.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    """PDF 파일을 업로드하고 벡터스토어에 인덱싱합니다."""
    current_user = await get_current_user_from_cookie(request)

    if not file.filename:
        raise HTTPException(status_code=400, detail="파일명이 없습니다.")

    user_dir = os.path.join(DOCUMENTS_DIR, current_user.id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    pdfs = [f for f in os.listdir(user_dir) if f.lower().endswith(".pdf")]
    if len(pdfs) >= 10:
        raise HTTPException(
            status_code=400, detail="최대 10개의 PDF만 업로드할 수 있습니다."
        )

    file_path = os.path.join(user_dir, file.filename)
    print(f"[UPLOAD] 실제 저장 경로: {file_path}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 업로드 후 자동 문서 처리
    result = ingest_documents(user_dir, current_user.id)
    print(f"result: {result}")
    return JSONResponse({"result": result, "filename": file.filename})


@router.post("/delete_pdf")
async def delete_pdf(
    request: Request,
    filename: str = None,
    form_filename: str = Form(None, alias="filename"),
):
    """PDF 파일을 삭제하고 벡터스토어에서 해당 벡터도 제거합니다.
    filename 파라미터는 쿼리 파라미터나 폼 데이터로 전달할 수 있습니다.
    """
    # 쿼리 파라미터 또는 폼 데이터에서 filename 가져오기
    actual_filename = filename or form_filename
    if not actual_filename:
        raise HTTPException(status_code=400, detail="파일명이 필요합니다.")

    current_user = await get_current_user_from_cookie(request)

    user_dir = os.path.join(DOCUMENTS_DIR, current_user.id)
    file_path = os.path.join(user_dir, actual_filename)

    # 1. PDF 파일 삭제
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")
    os.remove(file_path)

    # 2. ChromaDB에서 해당 문서 벡터 삭제
    if OLLAMA_EMBEDDING_MODEL is None:
        raise HTTPException(
            status_code=500,
            detail="OLLAMA_EMBEDDING_MODEL 환경변수가 설정되어 있지 않습니다.",
        )
    embeddings = OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL
    )
    vectorstore = Chroma(
        collection_name=f"rag_docs_{current_user.id}",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    # 3. ChromaDB 벡터 삭제 (where 조건 사용)
    try:
        vectorstore._collection.delete(where={"filename": actual_filename})
        print(f"✅ ChromaDB에서 {actual_filename} 벡터가 삭제되었습니다.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ChromaDB 삭제 중 오류 발생: {str(e)}"
        )

    return {"result": f"{actual_filename} 삭제 완료"}
