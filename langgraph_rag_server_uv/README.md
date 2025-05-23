# LangGraph RAG Server (UV 버전)

이 프로젝트는 [langgraph_rag_server](https://github.com/your-username/langgraph_rag_server)의 UV 버전입니다. 
기존 프로젝트의 모든 기능을 그대로 유지하면서, 패키지 관리 도구를 UV로 변경했습니다.

## UV란?

UV는 Python 패키지 관리자로, pip의 대안으로 사용할 수 있는 빠르고 현대적인 도구입니다.

### UV의 주요 장점
- **빠른 설치 속도**: pip보다 최대 10-100배 빠른 패키지 설치
- **더 나은 의존성 해결**: 더 정확하고 빠른 의존성 해결
- **더 작은 디스크 공간**: 효율적인 패키지 저장 방식
- **더 나은 보안**: 현대적인 보안 기능 지원

## 설치 방법

1. Python 3.10 설치 (필수)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv
```

2. UV 설치
```bash
pip install uv
```

3. 가상환경 생성 및 활성화
```bash
# 가상환경 생성
uv venv

# 가상환경 활성화
source .venv/bin/activate
```

4. 의존성 설치
```bash
uv pip install -r requirements.txt
```

## UV 명령어 사용법

### 1. 패키지 설치
```bash
# 단일 패키지 설치
uv pip install package_name

# 여러 패키지 설치
uv pip install package1 package2

# requirements.txt에서 설치
uv pip install -r requirements.txt
```

### 2. 패키지 제거
```bash
uv pip uninstall package_name
```

### 3. 패키지 업데이트
```bash
uv pip install --upgrade package_name
```

### 4. 가상환경 관리
```bash
# 새 가상환경 생성
uv venv

# 가상환경 활성화
source .venv/bin/activate

# 가상환경 비활성화
deactivate
```

### 5. Python 스크립트 실행
```bash
# 가상환경 내에서 스크립트 실행
uv run python script.py

# 모듈로 실행
uv run python -m module_name
```

### 6. 테스트 실행
```bash
# 전체 테스트 실행
uv run pytest

# 특정 테스트 파일 실행
uv run pytest tests/test_api.py

# 특정 테스트 함수 실행
uv run pytest tests/test_api.py::test_function_name

# 테스트 커버리지 확인
uv pip install pytest-cov
uv run pytest --cov=app tests/
```

## 서버 실행

```bash
# 개발 모드로 실행
uv run uvicorn app.main:app --reload

# 프로덕션 모드로 실행
uv run uvicorn app.main:app --host 0.0.0.0 --port 8100
```

## 기존 프로젝트와의 차이점

이 프로젝트는 기존 [langgraph_rag_server](https://github.com/your-username/langgraph_rag_server)와 동일한 기능을 제공하지만, 다음과 같은 차이점이 있습니다:

1. **패키지 관리**: conda 대신 UV 사용
2. **의존성 관리**: env.yml 대신 requirements.txt 사용
3. **가상환경**: conda 환경 대신 UV 가상환경 사용

나머지 기능(API, 웹 인터페이스, RAG 시스템 등)은 기존 프로젝트와 동일합니다.

## 기타 정보

기존 프로젝트의 다음 섹션들은 동일하게 적용됩니다:
- API 문서
- 프로젝트 구조
- 기술 스택
- 주요 기능
- 데이터베이스 설정
- Ollama 설정
- 보안 구현
- 사용 방법

자세한 내용은 [기존 프로젝트의 README](https://github.com/your-username/langgraph_rag_server)를 참조하세요. 