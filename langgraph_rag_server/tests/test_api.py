import platform
import sys
import tempfile
from pathlib import Path

# 프로젝트 루트 경로를 Python 경로에 추가
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.auth import create_new_user
from app.core.config import ensure_directories
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

    # 기존 문서 디렉토리 정리
    import shutil
    from app.core.config import DOCUMENTS_DIR

    # 사용자 디렉토리를 비웁니다 (파일만 삭제, 디렉토리 구조는 유지)
    for user_id in ["1", "2"]:  # 테스트에서 사용할 사용자 ID
        user_dir = os.path.join(DOCUMENTS_DIR, user_id)
        if os.path.exists(user_dir):
            for file in os.listdir(user_dir):
                file_path = os.path.join(user_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    # 테스트 사용자 2명 생성
    try:
        create_new_user("user1@example.com", "password123")
        create_new_user("user2@example.com", "password456")
    except Exception:
        # 이미 생성된 사용자라면 무시
        pass


# 로그인 유틸리티 함수
def login_user(email, password):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_pdf_upload_and_limit():
    headers = login_user("user1@example.com", "password123")
    for i in range(10):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            create_test_pdf(tmp.name, text=f"테스트 PDF {i}\n고구려 장수왕")
            tmp.seek(0)
            with open(tmp.name, "rb") as f:
                response = client.post(
                    "/upload",
                    files={"file": (f"test_{i}.pdf", f, "application/pdf")},
                    headers=headers,
                )
            assert response.status_code == 200
    # 11번째 업로드는 실패해야 함
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name, text="테스트 PDF 11\n고구려 장수왕")
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload",
                files={"file": ("test_11.pdf", f, "application/pdf")},
                headers=headers,
            )
        assert response.status_code == 400
        assert "최대 10개의 PDF만 업로드" in response.json()["detail"]


def test_pdf_list():
    headers = login_user("user1@example.com", "password123")
    response = client.get("/pdf_list", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "pdfs" in data
    assert len(data["pdfs"]) == 10


def test_pdf_delete():
    headers = login_user("user1@example.com", "password123")
    # 1개 삭제
    response = client.post(
        "/delete_pdf", params={"filename": "test_0.pdf"}, headers=headers
    )
    assert response.status_code == 200
    # 목록에서 빠졌는지 확인
    response = client.get("/pdf_list", headers=headers)
    assert "test_0.pdf" not in response.json()["pdfs"]


def test_rag_query_no_docs():
    headers = login_user("user1@example.com", "password123")
    # 모든 PDF 삭제 후 질의 시 안내 메시지 반환
    response = client.get("/pdf_list", headers=headers)
    for pdf in response.json()["pdfs"]:
        client.post("/delete_pdf", params={"filename": pdf}, headers=headers)
    query = {"question": "테스트 질문입니다."}
    response = client.post("/api/v1/rag/query", json=query, headers=headers)
    assert response.status_code == 200
    assert "문서가 없습니다" in response.json()["answer"]


def test_rag_query_with_docs():
    headers = login_user("user1@example.com", "password123")
    # PDF 1개 업로드
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name, text="테스트 PDF\n고구려 장수왕")
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload",
                files={"file": ("test_rag.pdf", f, "application/pdf")},
                headers=headers,
            )
        assert response.status_code == 200

    # 질의
    query = {"question": "고구려 장수왕은 누구입니까?"}
    response = client.post("/api/v1/rag/query", json=query, headers=headers)
    assert response.status_code == 200
    data = response.json()
    # answer와 sources가 정상적으로 반환되는지 확인
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0
    # (선택) answer에 '고구려' 또는 '장수왕'이 포함되는지 등 추가 검증 가능

    # 정리: 업로드한 PDF 삭제
    client.post("/delete_pdf", params={"filename": "test_rag.pdf"}, headers=headers)


def test_multi_user_data_isolation():
    # 첫 번째 사용자로 로그인하고 PDF 업로드
    user1_headers = login_user("user1@example.com", "password123")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name, text="사용자1의 고유 문서: 백제 무령왕")
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload",
                files={"file": ("user1_doc.pdf", f, "application/pdf")},
                headers=user1_headers,
            )
        assert response.status_code == 200

    # 두 번째 사용자로 로그인하고 다른 PDF 업로드
    user2_headers = login_user("user2@example.com", "password456")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name, text="사용자2의 고유 문서: 신라 진흥왕")
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload",
                files={"file": ("user2_doc.pdf", f, "application/pdf")},
                headers=user2_headers,
            )
        assert response.status_code == 200

    # 각 사용자의 문서 목록 확인
    response = client.get("/pdf_list", headers=user1_headers)
    user1_docs = response.json()["pdfs"]
    assert "user1_doc.pdf" in user1_docs
    assert "user2_doc.pdf" not in user1_docs

    response = client.get("/pdf_list", headers=user2_headers)
    user2_docs = response.json()["pdfs"]
    assert "user2_doc.pdf" in user2_docs
    assert "user1_doc.pdf" not in user2_docs

    # 사용자1과 사용자2에 대해 비슷한 질문을 하고 결과 확인
    query = {"question": "누가 왕입니까?"}

    # 사용자1의 질문 결과에는 "백제" 또는 "무령왕"이 포함되어야 함
    response = client.post("/api/v1/rag/query", json=query, headers=user1_headers)
    assert response.status_code == 200
    user1_answer = response.json()["answer"]
    assert "백제" in user1_answer or "무령왕" in user1_answer

    # 사용자2의 질문 결과에는 "신라" 또는 "진흥왕"이 포함되어야 함
    response = client.post("/api/v1/rag/query", json=query, headers=user2_headers)
    assert response.status_code == 200
    user2_answer = response.json()["answer"]
    assert "신라" in user2_answer or "진흥왕" in user2_answer

    # 정리: 업로드한 PDF 삭제
    client.post(
        "/delete_pdf", params={"filename": "user1_doc.pdf"}, headers=user1_headers
    )
    client.post(
        "/delete_pdf", params={"filename": "user2_doc.pdf"}, headers=user2_headers
    )


def test_authentication_required():
    # 인증 없이 요청 시 401 에러 반환
    response = client.get("/pdf_list")
    assert response.status_code == 401

    response = client.post("/api/v1/rag/query", json={"question": "테스트"})
    assert response.status_code == 401

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        create_test_pdf(tmp.name)
        tmp.seek(0)
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/upload", files={"file": ("test.pdf", f, "application/pdf")}
            )
        assert response.status_code == 401


def test_register_login_logout():
    # 새 사용자 등록
    email = "test_user@example.com"
    password = "test_password"

    # 기존 사용자 있을 수 있으니 삭제 먼저 시도 (에러 무시)
    try:
        from app.core.auth import fake_users_db

        if email in fake_users_db:
            del fake_users_db[email]
    except Exception:
        pass

    # 회원가입
    response = client.post(
        "/register", data={"email": email, "password": password, "password2": password}
    )
    assert response.status_code in [200, 302]

    # 로그인
    response = client.post(
        "/api/v1/auth/token", data={"username": email, "password": password}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 로그인 토큰으로 접근 확인
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.get("/pdf_list", headers=headers)
    assert response.status_code == 200
