# LangGraph RAG Server

## 기술 스택

- **백엔드**: FastAPI 0.115.9
- **데이터베이스**: PostgreSQL + SQLAlchemy 1.4.23
- **벡터 데이터베이스**: ChromaDB 0.6.3
- **LLM/임베딩**: Ollama (qwen3:30b-a3b, nomic-embed-text)
- **인증**: JWT + bcrypt
- **문서 처리**: PyPDF 5.4.0
- **테스트**: pytest 8.3.5

## 주요 기능

1. **PDF 기반 질의응답 (RAG)**
   - PDF 문서를 업로드하고 질문하면 문서 내용을 기반으로 답변 생성
   - 답변과 함께 참고한 문서의 출처(근거) 제공

2. **멀티유저 지원**
   - 사용자별 계정 및 데이터 분리
   - JWT 기반 인증 시스템
   - 각 사용자마다 독립적인 문서 저장소와 벡터 데이터베이스

## 설치 및 실행 방법

### 1. 필수 요구사항
- Python 3.10
- PostgreSQL
- Ollama
- Conda

### 2. 환경 설정

1. PostgreSQL 설치 및 설정
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL 서비스 시작
sudo service postgresql start

# PostgreSQL 사용자 생성 및 데이터베이스 생성
sudo -u postgres psql
postgres=# CREATE USER your_username WITH PASSWORD 'your_password';
postgres=# CREATE DATABASE your_database_name;
postgres=# GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
postgres=# \q
```

2. 환경 변수 설정
```bash
# .env 파일 생성
cp env.example .env

# .env 파일 편집
nano .env
```

3. Ollama 설치 및 모델 다운로드
```bash
# Ollama 설치 (Linux)
curl https://ollama.ai/install.sh | sh

# LLM 모델 설치
ollama pull qwen3:30b-a3b

# 임베딩 모델 설치
ollama pull nomic-embed-text
```

### 3. 설치 및 실행 순서

1. Conda 환경 생성 및 활성화
```bash
conda env create -f env.yml
conda activate langrag_venv
```

2. 데이터베이스 마이그레이션 설정
```bash
# 1. 기존 alembic 디렉토리 삭제 (이미 존재하는 경우)
rm -rf alembic

# 2. alembic 초기화
alembic init alembic

# 3. alembic.ini 파일에서 sqlalchemy.url 수정
# sqlalchemy.url = postgresql://your_username:your_password@localhost/your_database_name

# 4. 마이그레이션 생성
export PYTHONPATH=$PYTHONPATH:$(pwd)
alembic revision --autogenerate -m "Create users table"

# 5. 마이그레이션 적용
alembic upgrade head
```

3. 서비스 실행
```bash
# 터미널 1: Ollama 서버 실행
OLLAMA_HOST=0.0.0.0 ollama serve

# 터미널 2: FastAPI 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8100
```

4. 웹 인터페이스 접속
- 브라우저에서 [http://localhost:8100](http://localhost:8100) 접속
- 회원가입: [http://localhost:8100/register](http://localhost:8100/register)
- 로그인: [http://localhost:8100/login](http://localhost:8100/login)

### 4. 테스트 실행

1. 단위 테스트 실행
```bash
pytest tests/
```

2. 특정 테스트 실행
```bash
# API 테스트만 실행
pytest tests/test_api.py

# 특정 테스트 함수만 실행
pytest tests/test_api.py::test_function_name
```

3. 테스트 커버리지 확인
```bash
pytest --cov=app tests/
```

## 기술적 상세

### 1. RAG 시스템 구성
- **문서 처리**: PyPDF를 사용하여 PDF 문서를 텍스트로 변환
- **청크 분할**: RecursiveCharacterTextSplitter를 사용하여 문서를 의미 있는 청크로 분할
- **임베딩**: Ollama의 nomic-embed-text 모델을 사용하여 텍스트를 벡터로 변환
- **벡터 저장**: ChromaDB를 사용하여 벡터를 저장하고 검색
- **답변 생성**: Ollama의 qwen3:30b-a3b 모델을 사용하여 컨텍스트 기반 답변 생성

### 2. 보안 구현
- **비밀번호 해싱**: bcrypt를 사용하여 비밀번호를 안전하게 저장
- **JWT 인증**: python-jose를 사용하여 JWT 토큰 생성 및 검증
- **데이터 격리**: 사용자별 독립적인 문서 저장소와 벡터스토어 컬렉션

### 3. 데이터베이스 스키마
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 사용 방법

### 1. 웹 인터페이스 사용 방법

1. 회원가입 및 로그인
   - 이메일과 비밀번호를 입력하여 계정 생성
   - 로그인 페이지에서 계정 로그인

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

## ChromaDB 폴더 정리(중요)

- PDF/문서 삭제 시 `data/chroma_db` 하위 UUID 폴더는 **자동 삭제되지 않습니다** (ChromaDB 설계상 정상)
- **컬렉션 전체 삭제** 또는 **DB 재빌드**로만 안전하게 정리 가능
- 자세한 방법은 [Chroma Cookbook - Rebuilding Chroma DB](https://cookbook.chromadb.dev/strategies/rebuilding/) 참고

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

## 참고 사항
- Ollama 서버는 별도 터미널에서 반드시 실행되어야 합니다.
- `.env` 파일이 없으면 LLM이 정상 동작하지 않습니다.
- PDF를 업로드/처리하지 않으면 질의 시 안내 메시지가 반환됩니다.
- 모든 서비스(FastAPI, Ollama, PostgreSQL)가 정상적으로 실행 중인지 확인하세요. 