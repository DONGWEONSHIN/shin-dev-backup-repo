# LangGraph RAG 시스템

본 프로젝트는 LangGraph와 LangChain을 사용하여 PDF 문서 처리에 특화된 적응형 RAG(Retrieval-Augmented Generation) 시스템을 구현합니다.

## 주요 기능

- PDF 문서 처리 및 청크 분할
- Chroma 벡터 스토어를 이용한 의미 검색
- LangGraph를 활용한 적응형 RAG 워크플로우
- 대화형 질의응답 시스템
- Ollama를 이용한 로컬 LLM 및 임베딩

## 설치 및 실행 순서

### 1. 사전 요구사항 및 Ollama 실행

1. Ollama 설치:
   - [Ollama 공식 사이트](https://ollama.ai)에서 설치 방법 확인
2. Ollama 모델 다운로드:
   ```bash
   ollama pull qwen3:30b-a3b
   ```
3. Ollama 서버 실행:
   ```bash
   ollama serve
   ```
   - Ollama가 항상 실행 중이어야 합니다. (별도 터미널에서 실행 권장)
4. Ollama 서비스가 정상적으로 실행 중인지 확인:
   ```bash
   curl http://localhost:11434/api/version
   ```
   - 버전 정보가 출력되면 정상적으로 실행 중입니다.

### 2. Conda 환경 설정

```bash
conda env create -f env.yml
conda activate langgraphrag_venv
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 Ollama 모델명 추가
# 예시:
# OLLAMA_MODEL=qwen3:30b-a3b
# 또는
# OLLAMA_MODEL=qwen3:8b-q4_K_M
```

### 4. PDF 문서 준비 (택 1)

A. 테스트 PDF 생성 (선택사항):
```bash
python create_test_pdf.py
```
- LangGraph와 RAG에 대한 테스트 문서를 생성합니다
- `documents/test.pdf` 파일이 생성됩니다

B. 직접 PDF 추가:
- `documents` 디렉토리에 원하는 PDF 파일을 직접 복사
- 파일 개수에 제한은 없으나, 많은 파일을 처리할 경우 시간이 소요될 수 있습니다

### 5. 문서 처리 (필수)
```bash
python add_documents.py
```
- **이 단계는 반드시 실행해야 합니다!**
- `documents` 디렉토리의 모든 PDF 파일을 처리합니다
- 문서를 청크로 분할하고 벡터 스토어에 저장합니다
- PDF 파일을 추가하거나 수정할 때마다 이 스크립트를 다시 실행해야 합니다

### 6. RAG 시스템 사용
```bash
python test_rag.py
```
- 실제 질의응답을 수행합니다
- 미리 정의된 테스트 질문들을 실행합니다
- 시스템의 응답을 확인할 수 있습니다

## 시스템 구성 요소

1. **PDF 생성** (`create_test_pdf.py`):
   - 테스트용 PDF 문서 생성
   - LangGraph와 RAG 관련 내용 포함
   - 실제 사용 시에는 건너뛸 수 있음

2. **문서 처리** (`add_documents.py`):
   - PDF 파일 로딩 및 처리
   - 1000자 단위 청크 분할 (200자 오버랩)
   - 벡터 스토어 관리
   - 문서 추가/수정 시 재실행 필요

3. **RAG 시스템** (`rag_system.py`):
   - 시스템의 핵심 로직을 담고 있는 모듈
   - Ollama 기반 LLM 및 임베딩 사용
   - 직접 실행하지 않음 (test_rag.py에서 임포트하여 사용)
   - 문서 검색 (최대 3개의 관련 문서 검색)
   - 컨텍스트 기반 응답 생성
   - 적응형 워크플로우 관리
   - 상태 기반 결정 로직

4. **테스트** (`test_rag.py`):
   - RAG 시스템을 실제로 사용하는 스크립트
   - `rag_system.py`의 기능을 호출
   - 다양한 쿼리로 시스템 테스트
   - 응답 생성 및 오류 처리

## 프로젝트 구조

```
langgraph_project/
├── create_test_pdf.py   # 테스트 PDF 생성 (선택사항)
├── add_documents.py     # PDF 문서 처리 (필수 실행)
├── rag_system.py       # RAG 시스템 핵심 (직접 실행하지 않음)
├── test_rag.py        # 시스템 테스트 및 사용
├── documents/         # PDF 저장 디렉토리
├── chroma_db/        # 벡터 스토어 디렉토리 (자동 생성)
├── env.yml           # Conda 환경 설정
├── .env             # 환경 변수
├── .env.example     # 환경 변수 템플릿
└── README.md       # 문서
```

## 의존성

- Python 3.10
- LangChain 0.3.24
- LangGraph 0.4.1
- ChromaDB 0.6.3
- FastAPI 0.115.9
- Uvicorn 0.34.2
- PyPDF 5.4.0
- scikit-learn 1.4.1.post1
- Ollama (로컬 LLM 및 임베딩)
- langchain-ollama 0.3.2
- langchain-chroma 0.2.3
- langchain-openai 0.3.15
- langchain-community 0.3.23

## 참고 사항

- `chroma_db` 디렉토리는 벡터 저장소용으로 자동 생성됨
- PDF 문서는 효율적인 컨텍스트 관리를 위해 청크 단위로 처리됨
- 시스템 사용을 위해 Ollama가 설치되어 있어야 함
- 각 쿼리당 최대 3개의 관련 문서를 검색하여 컨텍스트로 사용
- 문서를 추가하거나 수정할 때마다 `add_documents.py`를 다시 실행해야 함
- Ollama 모델은 로컬에서 실행되므로 인터넷 연결이 필요하지 않음
- qwen3:30b-a3b 모델은 상당한 시스템 리소스를 필요로 함

## 주의사항

- `rag_system.py`는 직접 실행하지 않습니다 (다른 파일에서 임포트하여 사용)
- 문서 수정 시 항상 `add_documents.py`를 다시 실행해야 합니다
- Ollama 서비스가 실행 중이어야 합니다
- 충분한 시스템 리소스(RAM, GPU)가 필요합니다 