import platform
import tempfile
from pathlib import Path

from app.core.config import CHROMA_PERSIST_DIR, DOCUMENTS_DIR, ensure_directories
from app.main import app
from fastapi.testclient import TestClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

client = TestClient(app)


def create_test_pdf(path, text="테스트 PDF입니다. 고구려 장수왕은 고구려의 왕입니다."):
    system = platform.system()
    font_path = None
    if system == "Darwin":
        font_path = Path.home() / "Library/Fonts/NanumGothic-Regular.ttf"
    elif system == "Linux":
        font_path = Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf")
    else:
        font_path = None
    if font_path and font_path.exists():
        pdfmetrics.registerFont(TTFont("NanumGothic", font_path))
        font_name = "NanumGothic"
    else:
        font_name = "Helvetica"
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont(font_name, 10)
    y = 750
    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15
    c.save()


def setup_module(module):
    # 테스트 전 필요한 폴더 생성
    ensure_directories()


def test_pdf_upload_and_limit():
    for i in range(10):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            create_test_pdf(tmp.name, text=f"테스트 PDF {i}\n고구려 장수왕")
            tmp.seek(0)
            with open(tmp.name, "rb") as f:
                response = client.post(
                    "/upload", files={"file": (f"test_{i}.pdf", f, "application/pdf")}
                )
            assert response.status_code == 200
    # 11번째 업로드는 실패해야 함
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name, text="테스트 PDF 11\n고구려 장수왕")
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload", files={"file": ("test_11.pdf", f, "application/pdf")}
            )
        assert response.status_code == 400
        assert "최대 10개의 PDF만 업로드" in response.json()["detail"]


def test_pdf_list():
    response = client.get("/pdf_list")
    assert response.status_code == 200
    data = response.json()
    assert "pdfs" in data
    assert len(data["pdfs"]) == 10


def test_pdf_delete():
    # 1개 삭제
    response = client.post("/delete_pdf", params={"filename": "test_0.pdf"})
    assert response.status_code == 200
    # 목록에서 빠졌는지 확인
    response = client.get("/pdf_list")
    assert "test_0.pdf" not in response.json()["pdfs"]


def test_rag_query_no_docs():
    # 모든 PDF 삭제 후 질의 시 안내 메시지 반환
    response = client.get("/pdf_list")
    for pdf in response.json()["pdfs"]:
        client.post("/delete_pdf", params={"filename": pdf})
    query = {"question": "테스트 질문입니다."}
    response = client.post("/api/v1/rag/query", json=query)
    assert response.status_code == 200
    assert "문서가 없습니다" in response.json()["answer"]


def test_rag_query_with_docs():
    # PDF 1개 업로드
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name, text="테스트 PDF\n고구려 장수왕")
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload", files={"file": ("test_rag.pdf", f, "application/pdf")}
            )
        assert response.status_code == 200

    # 질의
    query = {"question": "고구려 장수왕은 누구입니까?"}
    response = client.post("/api/v1/rag/query", json=query)
    assert response.status_code == 200
    data = response.json()
    # answer와 sources가 정상적으로 반환되는지 확인
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    # (선택) answer에 '고구려' 또는 '장수왕'이 포함되는지 등 추가 검증 가능

    # 정리: 업로드한 PDF 삭제
    client.post("/delete_pdf", params={"filename": "test_rag.pdf"})
