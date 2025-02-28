# Speech-to-Text Web Application

## 📌 프로젝트 개요
이 프로젝트는 OpenAI Whisper 로컬 모델을 활용하여 음성 파일을 텍스트로 변환하는 STT(Speech-to-Text) 웹 애플리케이션입니다. FastAPI 기반의 REST API를 제공하며, 변환된 텍스트를 파일로 저장할 수 있습니다.

본 프로젝트에는 두 개의 주요 STT 프로그램이 포함됩니다:
1. **`whisper_stt.py`**: 기본적인 STT 변환 기능 제공
2. **`whisper_stt_v2.py`**: STT 변환 + 텍스트 전처리 + 요약 기능 + 환경변수 활용 + Base64 변환 기능 추가

각 프로그램의 차이에 대해서는 아래에서 자세히 설명합니다.

## 🛠️ 주요 기능
### `whisper_stt.py`
- **Whisper STT 모델**을 이용한 음성 인식 (로컬 실행)
- **MP3, WAV, M4A 등 다양한 오디오 포맷 지원**
- **FastAPI 기반 웹 서버**
- **텍스트 파일(.txt)로 변환 결과 저장**
- **텍스트 전처리 (불필요한 단어 제거, 문장 정리)**

### `whisper_stt_v2.py` (추가 기능 포함)
- `whisper_stt.py`의 모든 기능 포함
- **추출 요약 (TextRank)** 및 **추상 요약 (BART)** 기능 추가
- **환경변수 (.env) 파일 사용 가능** (Whisper 및 요약 모델 설정 가능)
- **변환된 결과를 Base64 인코딩하여 반환하는 기능 추가**
- **더 안전한 파일명 생성 (UUID 활용)**
- **Whisper 모델 및 요약 모델을 환경변수로 설정 가능**

## 📂 폴더 구조
```
speech_to_text_project/
│── models/               # Whisper 모델 캐시 저장 폴더 (필요한 경우)
│── temp/                 # 업로드된 오디오 파일 및 변환된 텍스트 저장
│── whisper_stt.py        # STT 변환 메인 코드
│── whisper_stt_v2.py     # STT 변환 + 요약 기능 포함 코드
│── requirements.txt      # 필수 패키지 목록
│── README.md             # 프로젝트 설명 문서
```

## 🚀 설치 및 실행 방법
### 1️⃣ **환경 설정**
Python 3.8 이상이 필요합니다. 가상 환경을 설정한 후, 필수 패키지를 설치하세요.
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2️⃣ **FFmpeg 설치 (오디오 변환 오류 방지)**
**Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```
**Mac (Homebrew 사용):**
```bash
brew install ffmpeg
```
**Windows (Chocolatey 사용):**
```powershell
choco install ffmpeg
```

### 3️⃣ **FastAPI 서버 실행**
#### `whisper_stt.py` 실행
```bash
uvicorn whisper_stt:app --host 0.0.0.0 --port 8000
```

#### `whisper_stt_v2.py` 실행
```bash
uvicorn whisper_stt_v2:app --host 0.0.0.0 --port 8000
```

## 📄 **API 사용 방법**
### **STT 변환** (`whisper_stt.py`, `whisper_stt_v2.py` 공통 기능)
#### 📌 **Swagger UI 사용 (브라우저에서 테스트 가능)**
1. 서버 실행 후, **브라우저에서 아래 URL 접속**
   ```
   http://127.0.0.1:8000/docs
   ```
2. **`/stt/` 엔드포인트 선택 → "Try it out" 버튼 클릭 → 오디오 파일 업로드 → Execute 실행**
3. 변환된 텍스트 확인

#### 📌 **cURL 명령어로 테스트 (터미널 사용)**
```bash
curl -X 'POST'
  'http://127.0.0.1:8000/stt/'
  -H 'accept: application/json'
  -H 'Content-Type: multipart/form-data'
  -F 'file=@your_audio_file.mp3'
```

### **추가 기능 (whisper_stt.py 전용)**
#### 📌 **추출 요약 (Extractive Summary) 사용 방법**
```bash
curl -X 'POST'
  'http://127.0.0.1:8000/summarize/extractive/'
  -H 'accept: application/json'
  -H 'Content-Type: application/json'
  -d '{"text": "요약할 문장입니다.", "sentence_count": 3}'
```

#### 📌 **추상 요약 (Abstractive Summary) 사용 방법**
```bash
curl -X 'POST'
  'http://127.0.0.1:8000/summarize/abstractive/'
  -H 'accept: application/json'
  -H 'Content-Type: application/json'
  -d '{"text": "요약할 문장입니다.", "max_length": 150, "min_length": 50}'
```

### **파일 저장 위치 안내**
- 변환된 텍스트 파일: `temp/audio_transcript.txt`
- 추출 요약 파일: `temp/audio_extractive_summary.txt`
- 추상 요약 파일: `temp/audio_abstractive_summary.txt`

## 📌 환경변수 설정 (.env 파일)
`whisper_stt_v2.py`에서는 환경변수를 사용하여 설정할 수 있습니다. `.env` 파일을 프로젝트 폴더에 생성한 후, 다음과 같이 설정하세요:
```bash
WHISPER_MODEL=small
SUMMARY_MODEL=facebook/bart-large-cnn
```

## 🛠️ 추가 기능 개발 예정
- 웹 UI 추가
- 다국어 요약 기능 강화
- 데이터베이스 저장 기능 추가

---
📌 **문의 및 개선 사항은 언제든지 제안해 주세요! 🚀**

