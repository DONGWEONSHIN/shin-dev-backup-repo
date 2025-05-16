# LangGraph RAG Server

## 주요 기능

1. **PDF 기반 질의응답 (RAG)**
   - PDF 문서를 업로드하고 질문하면 문서 내용을 기반으로 답변 생성
   - 답변과 함께 참고한 문서의 출처(근거) 제공

2. **멀티유저 지원**
   - 사용자별 계정 및 데이터 분리
   - JWT 기반 인증 시스템
   - 각 사용자마다 독립적인 문서 저장소와 벡터 데이터베이스

## 사용 방법

### 1. 웹 인터페이스 사용 방법

1. 회원가입 및 로그인
   - 브라우저에서 [http://localhost:8100/register](http://localhost:8100/register) 접속
   - 이메일과 비밀번호를 입력하여 계정 생성
   - 로그인 페이지([http://localhost:8100/login](http://localhost:8100/login))에서 계정 로그인

2. PDF 업로드
   - 메인 페이지에서 PDF 파일을 선택하고 업로드
   - 업로드된 PDF는 자동으로 벡터스토어에 인덱싱됨

3. 질문 및 답변
   - 메인 페이지에서 질문 입력 후 전송
   - 시스템이 문서 내용을 기반으로 답변 생성
   - 답변 하단에 참고한 문서 출처가 표시됨

4. PDF 관리
   - 업로드된 PDF 목록 확인 및 불필요한 PDF 삭제 가능
   - 각 사용자는 최대 10개의 PDF 업로드 가능

### 2. API 사용 방법

1. 사용자 등록 (회원가입)
   ```bash
   curl -X POST http://localhost:8100/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "your-email@example.com", "password": "your-password"}'
   ```
   응답 예시:
   ```json
   {
     "id": "1",
     "email": "your-email@example.com",
     "hashed_password": "hashed-password-string",
     "is_active": true,
     "created_at": "2023-06-15T12:34:56.789012",
     "updated_at": "2023-06-15T12:34:56.789012"
   }
   ```

2. 인증 토큰 발급 (로그인)
   ```bash
   # 로그인하여 토큰 발급
   curl -X POST http://localhost:8100/api/v1/auth/token \
     -d "username=your-email@example.com&password=your-password" \
     -H "Content-Type: application/x-www-form-urlencoded"
   ```
   응답 예시:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

3. PDF 목록 조회
   ```bash
   curl -X GET http://localhost:8100/pdf_list \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

4. PDF 업로드
   ```bash
   curl -X POST http://localhost:8100/upload \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -F "file=@/path/to/your/document.pdf"
   ```

5. 질의응답 API
   ```bash
   curl -X POST http://localhost:8100/api/v1/rag/query \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"question": "여기에 질문을 입력하세요"}'
   ```
   응답 예시:
   ```json
   {
     "answer": "질문에 대한 답변 내용...\n\n[참고 문서]\n- document.pdf (페이지: 3, 관련도: 높음)",
     "sources": [
       {
         "filename": "document.pdf",
         "source": "/path/to/document.pdf",
         "page": 3,
         "score": 0.89,
         "preview": "문서 내용 미리보기..."
       }
     ]
   }
   ```

6. PDF 삭제 (두 가지 방법)
   
   방법 1: 쿼리 파라미터 사용 (권장)
   ```bash
   curl -X POST "http://localhost:8100/delete_pdf?filename=document.pdf" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```
   
   방법 2: 폼 데이터 사용
   ```bash
   curl -X POST http://localhost:8100/delete_pdf \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "filename=document.pdf"
   ```

## 멀티유저 시스템 아키텍처

- **사용자 인증**: JWT 토큰 기반 (access_token)
- **사용자 데이터 분리**:
  - 각 사용자별 독립적인 문서 저장 디렉토리 (`data/documents/{user_id}/`)
  - 사용자별 벡터스토어 컬렉션 (`rag_docs_{user_id}`)
- **보안**:
  - 토큰 검증을 통한 인증 체크
  - 사용자별 데이터 접근 제한
  - 웹 인터페이스에서는 HTTP-only 쿠키 사용

## 실행 방법

1. (최초 1회) Conda 환경 생성 및 활성화:
```bash
conda env create -f env.yml
conda activate langgraph_rag_server_venv
```

2. FastAPI 서버 실행 (uvicorn 사용):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8100
```
- 브라우저에서 [http://localhost:8100](http://localhost:8100) 접속
- 웹 UI: `/` (질문 입력 및 결과 확인)
- API: `/api/v1/rag/query` (POST, JSON: {"question": "..."})

3. Ollama 서버가 반드시 실행 중이어야 합니다 (백엔드 LLM 사용 시)
```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

---

## 폴더/파일 구조

```
langgraph_rag_server/
├── app/
│   ├── main.py                # FastAPI 엔트리포인트
│   ├── web/views.py           # 웹 라우터 및 PDF 관리
│   ├── core/document_ingest.py# PDF 임베딩 및 벡터스토어 저장
│   ├── core/rag_engine.py     # RAG 질의응답 엔진
│   ├── core/auth.py           # 인증 관련 유틸리티
│   ├── core/models.py         # 사용자 및 인증 관련 모델
│   ├── api/v1/rag.py          # RAG API 엔드포인트
│   ├── api/v1/auth.py         # 인증 API 엔드포인트
│   ├── templates/index.html   # 웹 UI 템플릿
│   ├── templates/login.html   # 로그인 페이지
│   ├── templates/register.html# 회원가입 페이지
│   └── ...                    # 기타 설정/정적파일
├── data/
│   ├── documents/             # 업로드된 PDF 저장 폴더 (사용자별 하위 폴더)
│   └── chroma_db/             # ChromaDB 벡터스토어 데이터
├── tests/
│   └── test_api.py            # 주요 기능 테스트 코드
├── env.yml                    # conda 및 pip 의존성
└── README.md
```

---

## 시스템 흐름 및 주요 기능

1. **사용자 인증**
   - 회원가입을 통해 사용자 계정 생성
   - 로그인하여 JWT 토큰 발급 및 인증
   - 인증된 사용자만 서비스 이용 가능

2. **PDF 업로드 및 인덱싱**
   - 웹 UI 또는 `/upload` 엔드포인트로 PDF 업로드
   - 업로드된 문서는 사용자별 폴더에 저장
   - 문서는 자동으로 사용자별 벡터스토어(ChromaDB)에 인덱싱

3. **질의응답 (RAG)**
   - 웹 UI 또는 `/api/v1/rag/query`(POST)로 질문 전송
   - 시스템은 사용자의 문서에서 관련 내용을 검색 후, LLM이 답변 생성
   - 답변과 함께 실제로 사용된 문서의 출처(근거)가 반환됨

4. **데이터 분리 및 보안**
   - 각 사용자는 자신의 문서만 접근 가능
   - 사용자별 독립적인 저장 공간과 벡터스토어 컬렉션
   - 한 사용자가 업로드한 문서는 다른 사용자의 검색 결과에 포함되지 않음

---

## 웹 UI 사용법

1. **회원가입 및 로그인**
   - `/register` 페이지에서 이메일과 비밀번호로 회원가입
   - `/login` 페이지에서 로그인
   - 로그인하면 메인 페이지로 자동 이동

2. **메인 화면**
   - 질문 입력 → 답변 및 출처 확인
   - PDF 업로드 → 자동 인덱싱
   - PDF 목록/삭제 기능

3. **PDF 관리**
   - 각 사용자는 최대 10개까지 PDF 업로드 가능
   - 자신이 업로드한 PDF만 볼 수 있음
   - 불필요한 PDF는 삭제 가능

4. **로그아웃**
   - 상단 로그아웃 버튼으로 세션 종료

---

## API 상세

### 인증 API
- `/api/v1/auth/register` (POST, JSON): 새 사용자 등록
  - 요청 형식: `{"email": "user@example.com", "password": "password123"}`
  - 응답: 생성된 사용자 정보 (id, email, hashed_password 등)

- `/api/v1/auth/token` (POST, form-data): 로그인 및 토큰 발급
  - 요청 형식: `username=user@example.com&password=password123`
  - 응답: `{"access_token": "토큰값", "token_type": "bearer"}`
  - 참고: username 필드에 이메일 주소를 사용합니다

### PDF 관리 API
- `/upload` (POST, multipart/form-data): PDF 업로드 및 인덱싱 (인증 필요)
- `/delete_pdf` (POST): PDF 및 벡터 삭제 (인증 필요)
- `/pdf_list` (GET): 업로드된 PDF 목록 반환 (인증 필요)

### RAG API
- `/api/v1/rag/query` (POST, JSON): 질의응답 API (인증 필요)

### API 인증 방법
- 모든 API 호출 시 `Authorization: Bearer {token}` 헤더 필요
- 토큰은 `/api/v1/auth/token` 엔드포인트에서 발급

### RAG API 반환 예시
```json
{
  "answer": "...답변 본문...\n\n[참고 문서]\n- 문서1.pdf (페이지: 3, 관련도: 높음)\n- 문서2.pdf (페이지: 5, 관련도: 중간)",
  "sources": [
    {
      "filename": "문서1.pdf",
      "source": "/full/path/to/문서1.pdf",
      "page": 3,
      "score": 0.92,
      "preview": "문서 내용 미리보기..."
    },
    ...
  ]
}
```
- `answer` 필드 마지막에 실제로 사용된 문서의 출처가 `[참고 문서]` 섹션으로 포함됩니다.
- `sources` 리스트에는 각 문서의 파일명, 전체 경로, 페이지, 유사도, 미리보기가 포함됩니다.

---

## ChromaDB 폴더 정리(중요)

- PDF/문서 삭제 시 `data/chroma_db` 하위 UUID 폴더는 **자동 삭제되지 않습니다** (ChromaDB 설계상 정상)
- **컬렉션 전체 삭제** 또는 **DB 재빌드**로만 안전하게 정리 가능
- 자세한 방법은 [Chroma Cookbook - Rebuilding Chroma DB](https://cookbook.chromadb.dev/strategies/rebuilding/) 참고

---

## 테스트

- `tests/test_api.py`에서 업로드, 삭제, 질의, 한도 등 자동화 테스트 제공
- `pytest`로 실행 가능

### 테스트 실행 방법

1. (가상환경 활성화 후) 프로젝트 루트에서 아래 명령어 실행:

```bash
PYTHONPATH=. pytest tests/
```

- 모든 테스트가 통과하면 API가 정상적으로 동작함을 의미합니다.
- 테스트 중 경고(warning)는 Pydantic 등 외부 라이브러리의 버전 이슈로, 기능 동작에는 영향이 없습니다.

---

## 환경 및 의존성

- 가상환경명: `langgraph_rag_server_venv`
- 주요 패키지: fastapi, langchain, chromadb, langchain-chroma, langchain-ollama, pypdf, reportlab 등
- 자세한 버전은 `env.yml` 참고

---

## 환경 변수 설정 (.env)

- 프로젝트 루트에 `.env` 파일을 생성하고 아래와 같이 작성하세요:

```env
# Ollama에서 사용할 LLM(질의응답) 모델명 (예: qwen3:30b-a3b)
OLLAMA_LLM_MODEL=qwen3:30b-a3b
# Ollama에서 사용할 임베딩 모델명 (예: nomic-embed-text)
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
# Ollama 서버 주소 (기본값: http://localhost:11434)
OLLAMA_BASE_URL=http://localhost:11434
```

- 샘플 파일: `.env.sample` 참고

- **임베딩 모델 추천:**
    - nomic-embed-text (빠르고 RAG에 최적화, Ollama 공식 지원)
    - mxbai-embed-large (더 높은 품질이 필요할 때)
    - all-minilm (가볍고 빠른 임베딩)
- **LLM 모델 추천:**
    - qwen3:30b-a3b (고성능, 한국어 지원, RAG에 적합)
    - 필요에 따라 qwen3:8b, mistral 등도 사용 가능

---

## 참고 사항
- Ollama 서버는 별도 터미널에서 반드시 실행되어야 합니다.
- `.env` 파일이 없으면 LLM이 정상 동작하지 않습니다.
- PDF를 업로드/처리하지 않으면 질의 시 안내 메시지가 반환됩니다.

(아래에 기존 프로젝트 설명, 구조, 의존성 등 이어서 작성) 