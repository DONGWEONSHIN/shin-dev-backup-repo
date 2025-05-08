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

## 환경 및 의존성

- 가상환경명: `langgraph_rag_server_venv`
- 주요 라이브러리 및 버전은 `env.yml` 파일에 정리되어 있습니다.
- 환경을 재설정하려면 `conda env update -f env.yml --prune` 명령을 사용할 수 있습니다.

## 시스템 흐름 및 주요 기능

1. **PDF 업로드 및 인덱싱**
   - 웹 UI 또는 `/upload` 엔드포인트로 PDF 업로드
   - 업로드된 문서는 자동으로 벡터스토어(ChromaDB)에 인덱싱
2. **질의응답 (RAG)**
   - 웹 UI 또는 `/api/v1/rag/query`(POST)로 질문 전송
   - 시스템은 문서에서 관련 내용을 검색 후, LLM이 답변 생성
   - 답변과 함께 실제로 사용된 문서의 출처(근거)가 반환됨

## 환경 변수 설정 (.env)

- 프로젝트 루트에 `.env` 파일을 생성하고 아래와 같이 작성하세요:

```env
# Ollama에서 사용할 LLM 모델명 (예: mistral, qwen3:30b-a3b 등)
OLLAMA_MODEL=mistral
```

- 샘플 파일: `.env.sample` 참고

## API/웹 경로 및 반환 예시

- **웹 UI**: `/` (PDF 업로드, 질의, 결과 확인)
- **API**: `/api/v1/rag/query` (POST, JSON: {"question": "..."})
- **PDF 업로드**: `/upload` (POST, multipart/form-data)

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

## 참고 사항
- Ollama 서버는 별도 터미널에서 반드시 실행되어야 합니다.
- `.env` 파일이 없으면 LLM이 정상 동작하지 않습니다.
- PDF를 업로드/처리하지 않으면 질의 시 안내 메시지가 반환됩니다.

(아래에 기존 프로젝트 설명, 구조, 의존성 등 이어서 작성) 