# nlp 폴더 안내

이 디렉토리는 자연어 처리(NLP) 및 테이블 데이터 기반 분류 실습을 위한 예제 코드와 데이터, 환경설정 파일을 포함합니다. 대표적으로 스팸 메시지 분류와 GCP Vertex AI 기반 테이블 모델 추론 예제가 제공됩니다.

## 주요 파일 및 구성

- **spamNham.ipynb**
  - SMS 스팸/햄 데이터셋(`spam.csv`)을 활용한 텍스트 분류 실습 노트북입니다.
  - 데이터 전처리, 토큰화, 시퀀스 변환, Keras 기반 모델링, 예측 결과 파일 생성까지의 전체 흐름을 다룹니다.
  - 주요 라이브러리: pandas, numpy, matplotlib, scikit-learn, tensorflow
  - 데이터 파일: `spam.csv`(원본), `spam.txt`(가공)

- **tabular_model_inference.ipynb**
  - GCP Vertex AI에 배포된 테이블 분류 모델에 Pandas DataFrame 데이터를 API로 추론 요청하는 예제입니다.
  - Titanic 데이터셋을 활용하며, Google Cloud Python SDK 사용법과 API 호출 흐름, GCS 버킷 마운트(gcsfuse) 예시가 포함되어 있습니다.
  - 주요 라이브러리: pandas, google-cloud-aiplatform, google.protobuf

- **env.yml**
  - 위 노트북 실행에 필요한 Conda 환경설정 파일입니다.
  - 주요 패키지: python=3.10, pandas, numpy, matplotlib, scikit-learn, tensorflow, google-cloud-aiplatform, protobuf, jupyter, gcsfs 등

- **spam.csv / spam.txt**
  - 스팸/햄 분류 실습에 사용되는 데이터 파일입니다.

## 환경설정 및 실행 가이드

1. Conda 환경 생성 및 활성화
```bash
cd nlp
conda env create -f env.yml
conda activate nlp-env
```

2. Jupyter Notebook 실행
```bash
jupyter notebook
```

3. 노트북별 실습
- `spamNham.ipynb`: 스팸/햄 분류 실습
- `tabular_model_inference.ipynb`: GCP Vertex AI 테이블 모델 추론 실습

## 참고 사항
- Google Cloud 관련 실습은 GCP 계정 및 Vertex AI, GCS 버킷 권한이 필요합니다.
- 데이터 파일(`spam.csv`)은 노트북에서 자동 다운로드 또는 직접 제공됩니다.
- 추가적인 데이터/코드 실험은 각 노트북을 복사하여 자유롭게 진행할 수 있습니다.

---

문의 및 개선 제안은 상위 레포지토리의 이슈 트래커를 활용해 주세요. 