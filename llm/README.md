# LLM Fine-tuning & Vision Demo

이 프로젝트는 Hugging Face Transformers와 Ollama를 활용한 대형 언어모델(LLM) 파인튜닝 및 비전 모델 실습 예제입니다.

## 폴더 구조

```
llm/
├── fineTunning.ipynb      # 텍스트 분류(감성분석) 파인튜닝 실습 노트북
├── llama3.ipynb           # Ollama 기반 비전/텍스트 모델 실습 노트북
├── env.yml                # 실습 환경 구축용 Conda 환경 파일
├── image.png              # 비전 모델 테스트용 이미지 예시
├── finetuned_model/       # 파인튜닝된 모델 및 토크나이저 저장 폴더
└── results/               # 학습 중간 결과 및 체크포인트 저장 폴더
```

## 주요 실습 내용

- **fineTunning.ipynb**
  - IMDB 감성분석 데이터셋을 활용한 BERT 기반 텍스트 분류 모델 파인튜닝
  - Hugging Face `transformers`, `datasets`, `Trainer` API 사용
  - 모델 저장 및 추론 예시 포함

- **llama3.ipynb**
  - Ollama Python 패키지를 활용한 Llama3 Vision 모델 실습
  - 이미지와 텍스트를 입력으로 받아 멀티모달 추론 예시

## 환경 구축

아래 명령어로 필요한 패키지와 환경을 한 번에 설치할 수 있습니다.

```bash
conda env create -f env.yml
conda activate llm-finetuning
```

- 주요 패키지: Python 3.9, torch (CUDA 11.8), transformers, datasets, accelerate, scipy, ollama, jupyterlab 등

## 실행 방법

1. 환경 활성화  
   ```bash
   conda activate llm-finetuning
   ```

2. JupyterLab 실행  
   ```bash
   jupyter lab
   ```

3. 브라우저에서 `fineTunning.ipynb` 또는 `llama3.ipynb`를 열어 실습 진행

## 참고/유의사항

- GPU 환경(CUDA 11.8)이 권장됩니다. (`nvidia-smi`로 GPU 인식 확인)
- Ollama 패키지는 별도의 Ollama 서버/엔진이 필요할 수 있습니다. [Ollama 공식 문서](https://github.com/ollama/ollama) 참고
- 파인튜닝된 모델 및 토크나이저는 `finetuned_model/` 폴더에 저장됩니다.
- 학습 중간 결과 및 체크포인트는 `results/` 폴더에 저장됩니다.

## 문의

- 작성자: D.W. SHIN
- 실습/코드 관련 문의는 이슈 또는 이메일로 연락 바랍니다. 