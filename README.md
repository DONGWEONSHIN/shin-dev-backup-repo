# Shin Dev Backup Repo

## 📌 프로젝트 개요
이 레포지토리는 데이터 과학, 인공지능(AI), 자연어 처리(NLP), 딥러닝 등 다양한 개발 학습 자료 및 프로젝트를 정리하고 백업하기 위해 만들어졌습니다. 본 저장소는 실무 및 학습 과정에서 축적된 코드, 실험 결과, 노하우를 체계적으로 저장하며, 재사용성과 공유 가능성을 높이는 것을 목적으로 합니다.

---

## ⚙️ 공통 실행 가이드

- **Python 버전**: Python 3.7 이상 권장
- **가상환경 설정** (선택)
  ```bash
  python -m venv venv
  source venv/bin/activate  # Windows는 venv\Scripts\activate
  pip install -r requirements.txt
  ```
- 각 프로젝트는 별도의 requirements.txt 또는 노트북 내 설치 코드가 포함되어 있습니다.

---

## 📂 프로젝트 요약

| 번호 | 디렉토리 | 설명 | 주요 기술 |
|------|----------|------|------------|
| 1 | aihub | AI 관련 데이터를 활용한 실습 | EDA, 모델 학습 |
| 2 | cats-dogs | 고양이/개 이미지 분류 | TensorFlow, Keras |
| 3 | gcp | GCP 기반 AI 모델 배포 실습 | GCP, 서버리스 |
| 4 | kaggle | Kaggle 대회 데이터 분석 | 시각화, ML 모델링 |
| 5 | llm | 대규모 언어 모델 실험 | Transformer, NLP |
| 6 | nlp | 텍스트 데이터 분석 및 모델 구축 | Transformer, 전처리 |
| 7 | note_for_memory | 개인 학습 노트 | 메모, 문제 해결 과정 |
| 8 | people_detector | YOLOv5를 활용한 사람 탐지 | YOLOv5, OpenCV |
| 9 | requirements-updater | 누락된 패키지 버전 자동 추가 도구 | pkg_resources |
| 10 | speech_to_text_project | 음성을 텍스트로 변환하는 STT 웹앱 | Whisper, FastAPI |
| 11 | text_gen_project | 텍스트 생성 모델 구현 | Hugging Face, PyTorch |
| 12 | fine_tune | 금융 뉴스 데이터 기반 LLM 파인튜닝 실험 | Mistral-7B, Qwen, PEFT, LoRA, WandB |
| 13 | foodmap-clustering-project | 서울 음식점 클러스터링 및 상권 분석 | KMeans, DBSCAN, MeanShift, Folium, Pandas |
| 14 | real_estate_project | 서울 마포구 아파트 실거래가 분석 및 예측 | XGBoost, SHAP, Folium, Pandas |

---

## 🔍 주요 디렉토리 상세

### 1. `aihub`
- AI 데이터 기반 실험 및 연구용 코드
- 데이터 전처리, 모델 학습, 평가 포함

### 2. `cats-dogs`
- 이미지 분류 딥러닝 실습
- TensorFlow/Keras 기반 모델 구현
```bash
cd cats-dogs
jupyter notebook
```

### 3. `gcp`
- Google Cloud Platform을 활용한 AI 서비스 배포 실습
- 환경 설정부터 서버리스 운영까지

### 4. `kaggle`
- Kaggle 대회 참여 및 분석 코드
- 전처리, 모델링, 제출 파일 생성 등

### 5. `llm`
- LLM 기반 자연어 처리 실험
- 최신 언어 모델 적용 실습

### 6. `nlp`
- NLP 기초부터 Transformer 기반 모델 구현
- 전처리, 특징 추출, 모델 학습 포함

### 7. `note_for_memory`
- 학습 중 정리한 개인 메모
- 실습 중 마주친 문제 및 해결 방식 요약

### 8. `people_detector`
- YOLOv5로 이미지 속 사람 수 카운트
```bash
cd people_detector
python detect_people.py --source path/to/image.jpg
```

### 9. `requirements-updater`
- requirements.txt 내 버전 누락 패키지를 자동 추가
```bash
cd requirements-updater
python add_versions_to_requirements.py
```

### 10. `speech_to_text_project`
- Whisper 모델 기반 STT 웹 애플리케이션
- 음성 변환 + 요약 기능 포함
```bash
cd speech_to_text_project
uvicorn whisper_stt:app --host 0.0.0.0 --port 8000
uvicorn whisper_stt_v2:app --host 0.0.0.0 --port 8000  # 확장 기능
```

### 11. `text_gen_project`
- Hugging Face 기반 텍스트 생성
- MPS 지원 (Apple Silicon)
```bash
cd text_gen_project
python text_generation_pipeline.py
```

### 12. `fine_tune`
- 금융 도메인 뉴스 데이터를 활용한 **대규모 언어 모델(LLM)** 파인튜닝 실험 프로젝트
- `Mistral-7B`와 `Qwen2.5-7B` 모델을 활용하여 사전학습 모델을 금융 데이터에 특화
- 주요 구성:
  - `mistral_finetune.ipynb` / `qwen_finetune.ipynb`: 각각 Mistral 및 Qwen 모델 기반 파인튜닝 노트북
  - `data/`: 실험에 사용된 원본 CSV 및 엑셀 뉴스 데이터
  - `models/`: 학습된 LoRA 어댑터 및 각 체크포인트 결과 저장
  - `images/`: 학습 로그, 시스템 모니터링 이미지
  - `wandb/`: 실시간 학습 로깅 데이터(WandB 연동)
- 학습 특징:
  - **PEFT(LoRA)** 방식으로 빠르고 효율적인 파인튜닝
  - Hugging Face `transformers`, `datasets`, `accelerate`, `trl` 등 최신 스택 활용
  - 시스템 모니터링 및 손실 지표 시각화 (WandB 연동)
- 실행 환경 예시:
```bash
cd fine_tune
conda create -n finetune-env python=3.10
conda activate finetune-env
pip install -r requirements.txt  # 또는 notebook 내 셀 참조
jupyter lab
```

### 13. `foodmap-clustering-project`
- 서울시 일반음식점 데이터를 기반으로 클러스터링을 통해 주요 상권을 식별하고, 이를 지도로 시각화하는 프로젝트
- 주요 분석 흐름:
  - `좌표 정제 및 변환`: EPSG:2097 → 위경도
  - `클러스터링`: KMeans, DBSCAN, MeanShift
  - `시각화`: Folium을 활용한 지도 기반 시각화
- 주요 특징:
  - Elbow 및 Silhouette 기법을 활용한 KMeans 최적화
  - 노이즈 제거 기능 포함(DBSCAN)
  - 자동 군집 수 탐색 기능(MeanShift)
```bash
cd foodmap-clustering-project
conda create -n foodmap-env python=3.10
conda activate foodmap-env
pip install -r requirements.txt
jupyter lab
```

### 14. `real_estate_project`
- 서울 마포구의 아파트 실거래 데이터를 분석하고, 예측 모델을 통해 가성비 좋은 지역을 지도 위에 시각화한 프로젝트
- 주요 특징:
  - `XGBoost`를 활용한 아파트 가격 예측
  - `SHAP`을 통한 모델 해석 및 변수 중요도 시각화
  - `Folium`을 이용한 가성비 지역 지도 시각화
  - `Kakao API`를 활용한 주소-좌표 변환
```bash
cd real_estate_project
conda env create -f env.yml
conda activate real_estate_project
jupyter notebook
```
---

## 📚 참고 자료

- [TensorFlow 공식 문서](https://www.tensorflow.org/)
- [Google Cloud AI 공식 문서](https://cloud.google.com/ai)
- [Kaggle 공식 웹사이트](https://www.kaggle.com/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)

---

본 저장소는 AI, 머신러닝, 자연어 처리 등 다양한 기술 스택을 학습하고 실험한 결과물을 아카이브한 공간입니다. 개발자 또는 연구자 여러분에게 참고가 되길 바랍니다. 😊

