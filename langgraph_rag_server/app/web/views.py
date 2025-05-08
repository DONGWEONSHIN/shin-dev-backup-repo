"""웹 라우터 및 PDF 업로드/삭제 뷰를 제공하는 모듈입니다."""

import os

from app.core.config import (
    CHROMA_PERSIST_DIR,
    DOCUMENTS_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    TEMPLATES_DIR,
)
from app.core.document_ingest import ingest_documents, delete_related_chroma_files
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """메인 인덱스 페이지(HTML)를 렌더링합니다."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/pdf_list")
def pdf_list():
    """업로드된 PDF 파일 목록을 반환합니다."""
    pdfs = [f for f in os.listdir(DOCUMENTS_DIR) if f.lower().endswith(".pdf")]
    return {"pdfs": pdfs}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """PDF 파일을 업로드하고 벡터스토어에 인덱싱합니다."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일명이 없습니다.")
    pdfs = [f for f in os.listdir(DOCUMENTS_DIR) if f.lower().endswith(".pdf")]
    if len(pdfs) >= 10:
        raise HTTPException(
            status_code=400, detail="최대 10개의 PDF만 업로드할 수 있습니다."
        )
    file_path = os.path.join(DOCUMENTS_DIR, file.filename)
    print(f"[UPLOAD] 실제 저장 경로: {file_path}")
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # 업로드 후 자동 문서 처리
    result = ingest_documents(DOCUMENTS_DIR)
    return JSONResponse({"result": result, "filename": file.filename})


@router.post("/delete_pdf")
def delete_pdf(filename: str):
    """PDF 파일을 삭제하고 벡터스토어에서 해당 벡터도 제거합니다."""
    file_path = os.path.join(DOCUMENTS_DIR, filename)

    # 1. PDF 파일 삭제
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")
    os.remove(file_path)

    # 2. ChromaDB에서 해당 문서 벡터 삭제
    if OLLAMA_MODEL is None:
        raise HTTPException(
            status_code=500, detail="OLLAMA_MODEL 환경변수가 설정되어 있지 않습니다."
        )
    embeddings = OllamaEmbeddings(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
    vectorstore = Chroma(
        collection_name="rag_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )



    # 3. ChromaDB 벡터 삭제 (where 조건 사용)
    try:
        vectorstore._collection.delete(where={"filename": filename})
        print(f"✅ ChromaDB에서 {filename} 벡터가 삭제되었습니다.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ChromaDB 삭제 중 오류 발생: {str(e)}"
        )

    return {"result": f"{filename} 삭제 완료"}
