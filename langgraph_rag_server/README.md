# LangGraph RAG Server

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

---

## 폴더/파일 구조

```
langgraph_rag_server/
├── app/
│   ├── main.py                # FastAPI 엔트리포인트
│   ├── web/views.py           # 웹 라우터 및 PDF 관리
│   ├── core/document_ingest.py# PDF 임베딩 및 벡터스토어 저장
│   ├── core/rag_engine.py     # RAG 질의응답 엔진
│   ├── api/v1/rag.py          # RAG API 엔드포인트
│   ├── templates/index.html   # 웹 UI 템플릿
│   └── ...                    # 기타 설정/정적파일
├── data/
│   ├── documents/             # 업로드된 PDF 저장 폴더
│   └── chroma_db/             # ChromaDB 벡터스토어 데이터
├── tests/
│   └── test_api.py            # 주요 기능 테스트 코드
├── env.yml                    # conda 및 pip 의존성
└── README.md
```

---

## 시스템 흐름 및 주요 기능

1. **PDF 업로드 및 인덱싱**
   - 웹 UI 또는 `/upload` 엔드포인트로 PDF 업로드
   - 업로드된 문서는 자동으로 벡터스토어(ChromaDB)에 인덱싱
2. **질의응답 (RAG)**
   - 웹 UI 또는 `/api/v1/rag/query`(POST)로 질문 전송
   - 시스템은 문서에서 관련 내용을 검색 후, LLM이 답변 생성
   - 답변과 함께 실제로 사용된 문서의 출처(근거)가 반환됨

---

## 웹 UI 사용법

- 브라우저에서 `/` 접속
- 질문 입력 → 답변 및 출처 확인
- PDF 업로드 → 자동 인덱싱
- PDF 목록/삭제 가능

---

## API 상세

- `/upload` (POST, multipart/form-data): PDF 업로드 및 인덱싱
- `/delete_pdf` (POST): PDF 및 벡터 삭제
- `/pdf_list` (GET): 업로드된 PDF 목록 반환
- `/api/v1/rag/query` (POST, JSON): 질의응답 API

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