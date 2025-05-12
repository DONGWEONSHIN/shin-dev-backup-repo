# Shin Dev Backup Repo

## 📄 목차
1. [📌 프로젝트 개요](#-프로젝트-개요)
2. [⚙️ 공통 실행 가이드](#️-공통-실행-가이드)
3. [📂 프로젝트 요약](#-프로젝트-요약)
4. [🔍 주요 디렉토리 상세](#-주요-디렉토리-상세)
5. [📚 참고 자료](#-참고-자료)

---

## 📌 프로젝트 개요
이 레포지토리는 데이터 과학, 인공지능(AI), 자연어 처리(NLP), 딥러닝 등 다양한 개발 학습 자료 및 프로젝트를 정리하고 백업하기 위해 만들어졌습니다. 실무 및 학습 과정에서 축적된 코드, 실험 결과, 노하우를 체계적으로 정리하여 재사용성과 공유 가능성을 높이는 것이 목적입니다.

---

## ⚙️ 공통 실행 가이드
- **Python 버전**: Python 3.7 이상 권장
- **가상환경 설정** (선택)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
- 각 프로젝트에는 개별 requirements.txt 또는 노트북 내 설치 코드가 포함되어 있습니다.

---

## 📂 프로젝트 요약
| 번호 | 디렉토리 | 설명 | 주요 기술 |
|------|----------|------|------------|
| 1 | aihub | AI 관련 데이터 실습 | EDA, 모델 학습 |
| 2 | cats-dogs | 고양이/개 이미지 분류 | TensorFlow, Keras |
| 3 | gcp | GCP 기반 데이터 관리 및 배포 | Google Cloud, Storage |
| 4 | kaggle | Kaggle 데이터셋 분석 | 전처리, 시각화 |
| 5 | llm | 대규모 언어 모델 실험 | LLM, Transformers |
| 6 | nlp | 자연어 처리 및 테이블 데이터 기반 분류 실습을 위한 프로젝트입니다. 대표적으로 스팸 메시지 분류와 GCP Vertex AI 기반 테이블 모델 추론 예제가 포함되어 있습니다.
| 7 | note_for_memory | 개인 학습 메모 모음 | 코드 요약, 이슈 해결 |
| 8 | people_detector | 사람 인식 모델 구현 | YOLOv5, OpenCV |
| 9 | requirements-updater | 패키지 버전 자동 업데이트 도구 | pkg_resources |
| 10 | speech_to_text_project | 음성 → 텍스트 변환 웹앱 | Whisper, FastAPI |
| 11 | text_gen_project | 텍스트 생성 파이프라인 | Hugging Face, PyTorch |
| 12 | fine_tune | LLM 금융 데이터 파인튜닝 | Mistral, Qwen, PEFT |
| 13 | foodmap-clustering-project | 서울 음식점 상권 분석 | KMeans, Folium |
| 14 | real_estate_project | 서울 아파트 부동산 예측 | XGBoost, SHAP, 지도 시각화 |
| 15 | langgraph_project | LangGraph 기반 PDF RAG 시스템 | LangGraph, LangChain, ChromaDB |
| 16 | langgraph_rag_server | LangGraph RAG 웹 서버 | FastAPI, LangGraph, ChromaDB |

---

## 🔍 주요 디렉토리 상세

### 1. `aihub`
- **설명**: AI Hub 데이터를 활용한 실습 프로젝트입니다. 데이터 전처리, 모델 학습 및 평가 과정을 포함합니다.
- **주요 특징**:
  - 공공 AI 데이터셋 활용
  - API 기반 다운로드 실습
  - 실험 재현을 위한 Jupyter 기반 노트북 제공
```bash
cd aihub
jupyter notebook aihub_api.ipynb
```

### 2. `cats-dogs`
- **설명**: TensorFlow/Keras 기반의 이미지 분류 실습입니다. 고양이와 개 이미지를 분류하는 모델 구현이 포함되어 있습니다.
- **주요 특징**:
  - CNN 모델 학습 구조 포함
  - ImageDataGenerator 활용
  - 분류 정확도 시각화
```bash
cd cats-dogs
jupyter notebook
```

### 3. `gcp`
- **설명**: Google Cloud Platform을 이용한 데이터 저장 및 관리 실습입니다. GCS 버킷 업로드, 라벨링 노트북 포함.
- **주요 특징**:
  - GCS CLI, Python 연동 실습
  - 버킷 내 자동 복사/정리 실험
  - 라벨링 기반 모델 전처리
```bash
cd gcp
jupyter notebook 버킷에데이터복사하고레이블링하기.ipynb
```

### 4. `kaggle`
- **설명**: Kaggle 대회용 데이터셋 다운로드, 전처리 및 분석 노트북 포함.
- **주요 특징**:
  - Google Colab 최적화
  - `.kaggle.json` 인증키 활용 방법 설명
  - 실전형 EDA 및 데이터 흐름 구성
```bash
cd kaggle
jupyter notebook colab에서kaggle데이터셋다운로드.ipynb
```

### 5. `llm`
- **설명**: LLaMA 등 LLM 모델을 활용한 파인튜닝 및 추론 실험을 포함합니다.
- **주요 특징**:
  - 최신 오픈소스 모델 실습
  - parameter-efficient tuning (LoRA, PEFT) 실험 기반
  - 추론 결과 및 로그 시각화 포함
```bash
cd llm
jupyter notebook fineTunning.ipynb
```

### 6. `nlp`
- **설명**: 자연어 처리 및 테이블 데이터 기반 분류 실습을 위한 프로젝트입니다. 대표적으로 스팸 메시지 분류와 GCP Vertex AI 기반 테이블 모델 추론 예제가 포함되어 있습니다.
- **주요 파일 및 특징**:
  - `spamNham.ipynb`: SMS 스팸/햄 데이터셋을 활용한 텍스트 분류 실습. 데이터 전처리, 토큰화, 시퀀스 변환, Keras 기반 모델링, 결과 파일 생성까지의 흐름을 다룹니다.
    - 주요 라이브러리: pandas, numpy, matplotlib, scikit-learn, tensorflow
    - 데이터: `spam.csv`(원본), `spam.txt`(가공)
  - `tabular_model_inference.ipynb`: GCP Vertex AI에 배포된 테이블 분류 모델에 Pandas DataFrame 데이터를 API로 추론 요청하는 예제. Titanic 데이터셋을 활용하며, Google Cloud Python SDK 사용법과 API 호출 흐름을 포함합니다.
    - 주요 라이브러리: pandas, google-cloud-aiplatform, google.protobuf
    - GCS 버킷 마운트(gcsfuse) 예시 포함
- **실행 가이드**:
```bash
cd nlp
jupyter notebook spamNham.ipynb
jupyter notebook tabular_model_inference.ipynb
```
- **환경설정**:
  - Python 3.10 이상 권장
  - 아래 `env.yml` 참고(Conda 환경)

### 7. `note_for_memory`
- **설명**: 학습 중 발견한 인사이트, 에러 해결 과정 등을 마크다운 형식으로 정리한 개인 메모 모음입니다.

### 8. `people_detector`
- **설명**: YOLOv5를 사용하여 이미지에서 사람을 탐지하는 프로젝트입니다.
- **주요 특징**:
  - YOLOv5 사전학습 모델 기반 추론
  - 실시간 객체 탐지 기능
  - OpenCV를 이용한 결과 시각화
```bash
cd people_detector
python detect_people.py --source path/to/image.jpg
```

### 9. `requirements-updater`
- **설명**: requirements.txt 파일에 버전 정보가 없는 패키지를 자동으로 채워주는 스크립트입니다.
- **주요 특징**:
  - pkg_resources 기반 패키지 탐색
  - 누락된 버전 정보를 자동 업데이트
  - 대규모 프로젝트 패키지 정리에 유용
```bash
cd requirements-updater
python add_versions_to_requirements.py
```

### 10. `speech_to_text_project`
- **설명**: Whisper 기반 STT(음성 → 텍스트) 웹 앱. FastAPI를 통한 API 제공.
- **주요 특징**:
  - Whisper 모델 기반 음성 인식
  - 요약 기능이 포함된 확장 모델 제공
  - 로컬 서버에서 REST API로 실행 가능
```bash
cd speech_to_text_project
uvicorn whisper_stt:app --host 0.0.0.0 --port 8000
```

### 11. `text_gen_project`
- **설명**: Hugging Face Transformers를 이용한 텍스트 생성 실습입니다.
- **주요 특징**:
  - 사용자 입력 기반 텍스트 자동 생성
  - 사전학습 모델 불러오기 및 추론 파이프라인 구현
  - Apple Silicon에서 MPS 가속 지원
```bash
cd text_gen_project
python text_generation_pipeline.py
```

### 12. `fine_tune`
- **설명**: 금융 뉴스 데이터를 활용한 LLM 파인튜닝 프로젝트입니다.
- **주요 특징**:
  - LoRA 기반의 경량 파인튜닝
  - 실험 결과 시각화 (WandB 연동)
  - 다양한 사전학습 모델 비교 실험
```bash
cd fine_tune
conda create -n finetune-env python=3.10
conda activate finetune-env
pip install -r requirements.txt
jupyter lab
```

### 13. `foodmap-clustering-project`
- **설명**: 서울시 마포구 음식점 데이터를 클러스터링하여 주요 상권을 분석합니다.
- **주요 특징**:
  - KMeans, DBSCAN, MeanShift 모델 비교
  - EPSG:2097 → 위경도 변환
  - Folium 기반 지도 시각화
```bash
cd foodmap-clustering-project
conda activate foodmap-env
jupyter lab
```

### 14. `real_estate_project`
- **설명**: 서울 마포구 아파트 실거래 데이터를 활용하여 예측 모델을 구축합니다.
- **주요 특징**:
  - XGBoost 기반 가격 예측
  - SHAP으로 변수 중요도 분석
  - Kakao API를 활용한 주소-좌표 변환
```bash
cd real_estate_project
conda env create -f env.yml
conda activate real_estate_project
jupyter notebook
```

### 15. `langgraph_project`
- **설명**: LangGraph와 LangChain을 활용한 PDF 문서 기반 RAG(Retrieval-Augmented Generation) 시스템입니다.
- **주요 특징**:
  - PDF 문서 처리 및 청크 분할
  - Chroma 벡터스토어를 이용한 의미 검색
  - LangGraph 기반 적응형 RAG 워크플로우
  - Ollama를 통한 로컬 LLM 연동
```bash
cd langgraph_project
conda env create -f env.yml
conda activate langgraphrag_venv
python add_documents.py
# 이후 RAG 시스템 실행
```

### 16. `langgraph_rag_server`
- **설명**: LangGraph 기반 RAG 시스템의 FastAPI 웹 서버 구현 프로젝트입니다.
- **주요 특징**:
  - 웹 UI 및 REST API 제공
  - PDF 업로드 및 벡터스토어 자동 인덱싱
  - 실시간 질의응답 및 출처 반환
```bash
cd langgraph_rag_server
conda env create -f env.yml
conda activate langgraph_rag_server_venv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8100
```

---

## 📚 참고 자료
- [TensorFlow 공식 문서](https://www.tensorflow.org/)
- [Google Cloud AI 공식 문서](https://cloud.google.com/ai)
- [Kaggle 공식 웹사이트](https://www.kaggle.com/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)

---

본 저장소는 다양한 기술 실험과 학습의 결과물을 정리한 공간으로, 개발자 또는 연구자에게 실질적인 도움이 되는 정보를 제공합니다.

