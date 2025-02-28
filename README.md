# Shin Dev Backup Repo

## 📌 프로젝트 개요

이 레포지토리는 다양한 개발 학습 자료와 프로젝트를 백업하고 정리하기 위해 만들어졌습니다. AI, 머신러닝, 딥러닝, 자연어 처리(NLP), Google Cloud Platform(GCP) 관련 프로젝트와 학습 기록이 포함되어 있으며, 학습과 실습 과정에서의 성장을 기록하는 데 중점을 두었습니다.

---

## 📂 주요 구성 요소

### 1. [AIHub (`aihub` 디렉토리)](./aihub)
- **설명**: AI 관련 데이터를 활용한 연구 및 실습 자료.
- **주요 내용**:
  - 데이터 전처리 및 탐색적 데이터 분석(EDA).
  - AI 모델 학습 및 결과 평가.

### 2. [Cats vs. Dogs 분류 (`cats-dogs` 디렉토리)](./cats-dogs)
- **설명**: 고양이와 개 이미지를 분류하는 딥러닝 프로젝트.
- **주요 내용**:
  - TensorFlow/Keras를 활용한 모델 구현.
  - 이미지 데이터셋 전처리 및 학습.

### 3. [Google Cloud Platform (`gcp` 디렉토리)](./gcp)
- **설명**: GCP를 활용한 AI 개발과 모델 배포 실습.
- **주요 내용**:
  - GCP 환경 설정.
  - 서버리스 AI 배포 및 관리.

### 4. [Kaggle 대회 (`kaggle` 디렉토리)](./kaggle)
- **설명**: Kaggle 대회를 위한 데이터 분석 및 머신러닝 모델링.
- **주요 내용**:
  - 데이터셋 전처리 및 시각화.
  - 다양한 머신러닝 알고리즘 적용.

### 5. [대규모 언어 모델(LLM) (`llm` 디렉토리)](./llm)
- **설명**: LLM 연구 및 실습 프로젝트.
- **주요 내용**:
  - LLM을 활용한 자연어 처리 태스크.
  - 최신 모델과 기술 적용.

### 6. [자연어 처리(NLP) (`nlp` 디렉토리)](./nlp)
- **설명**: 텍스트 데이터 분석 및 NLP 모델 구축.
- **주요 내용**:
  - 텍스트 데이터 전처리 및 특징 추출.
  - Transformer 기반 모델 구현.

### 7. [학습 기록 및 메모 (`note_for_memory` 디렉토리)](./note_for_memory)
- **설명**: 학습 중 기록한 개인 노트와 메모.
- **주요 내용**:
  - 학습 과정에서 배운 점과 참고 자료.
  - 문제 해결 과정 및 코드 스니펫.

### 8. [사람 감지 프로젝트 (`people_detector` 디렉토리)](./people_detector)
- **설명**: YOLOv5를 사용하여 이미지에서 사람을 감지하고 카운트하는 프로젝트.
- **주요 내용**:
  - **YOLOv5** 기반 객체 탐지 모델 활용.
  - OpenCV 및 PyTorch를 사용한 이미지 분석.
  - **이미지 속 사람의 수를 자동으로 카운트하는 기능 제공**.
- **실행 방법**:
  ```bash
  cd people_detector
  python detect_people.py --source path/to/image.jpg

### 9. [패키지 버전 자동 추가 도구 (`requirements-updater` 디렉토리)](./requirements-updater)
- **설명**: `requirements.txt` 파일에서 **누락된 패키지 버전을 자동으로 추가하는 도구**.
- **주요 내용**:
  - `requirements.txt` 내에서 버전 정보가 없는 패키지를 찾아 현재 환경의 버전 정보를 추가.
  - `pkg_resources` 라이브러리를 활용하여 설치된 패키지 정보를 가져와 업데이트.
  - **Python 3.7 이상에서 실행 가능**.
- **실행 방법**:
  ```bash
  cd requirements-updater
  python add_versions_to_requirements.py

### 10. [음성 → 텍스트 변환 프로젝트 (`speech_to_text_project` 디렉토리)](./speech_to_text_project)
- **설명**: OpenAI Whisper 모델을 활용하여 음성을 텍스트로 변환하는 **STT(Speech-to-Text) 웹 애플리케이션**.
- **주요 내용**:
  - **`whisper_stt.py`**: 기본적인 음성 변환 기능 제공.
  - **`whisper_stt_v2.py`**: 음성 변환 + **텍스트 요약, 환경변수 활용, Base64 변환** 기능 추가.
  - **FastAPI 기반 REST API 제공** (Swagger UI 및 cURL 명령어로 테스트 가능).
  - **MP3, WAV, M4A 등 다양한 오디오 포맷 지원**.
  - **추출 요약(TextRank) 및 추상 요약(BART) 기능 제공**.
- **실행 방법**:
  ```bash
  cd speech_to_text_project
  uvicorn whisper_stt:app --host 0.0.0.0 --port 8000  # 기본 실행
  uvicorn whisper_stt_v2:app --host 0.0.0.0 --port 8000  # 확장된 기능 실행

### 11. [텍스트 생성 프로젝트 (`text_gen_project` 디렉토리)](./text_gen_project)
- **설명**: Hugging Face의 **Transformers** 라이브러리를 사용하여 **텍스트 생성 모델을 구축**하는 프로젝트.
- **주요 내용**:
  - **Hugging Face 모델을 활용한 텍스트 생성**.
  - **PyTorch 기반 실행 환경 지원**.
  - Apple Silicon(M1/M2) 환경에서 **Metal Performance Shaders(MPS) 지원 확인**.
- **실행 방법**:
  ```bash
  cd text_gen_project
  python text_generation_pipeline.py


---

## 🚀 시작하기

### 1. 레포지토리 클론
```bash
git clone https://github.com/DONGWEONSHIN/shin-dev-backup-repo.git
```

### 2. 디렉토리 이동
```bash
cd shin-dev-backup-repo
```

### 3. 프로젝트 실행
각 디렉토리로 이동한 후, 필요한 파일을 확인하거나 실행합니다. 예를 들어, `cats-dogs` 프로젝트를 실행하려면 해당 디렉토리로 이동 후 Jupyter 노트북을 열어 실행하세요:
```bash
cd cats-dogs
jupyter notebook
```

---

## 📖 참고 자료

- [TensorFlow 공식 문서](https://www.tensorflow.org/)
- [Google Cloud AI 공식 문서](https://cloud.google.com/ai)
- [Kaggle 공식 웹사이트](https://www.kaggle.com/)

---

이 레포지토리는 학습과 프로젝트를 진행하면서 쌓아온 경험과 결과물을 정리한 공간입니다. AI, 머신러닝, NLP 등 다양한 주제에 대한 관심과 학습 과정을 함께 공유합니다. 😊
