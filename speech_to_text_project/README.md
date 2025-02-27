# Speech-to-Text Web Application

## 📌 프로젝트 개요
이 프로젝트는 OpenAI Whisper 로컬 모델을 활용하여 음성 파일을 텍스트로 변환하는 STT(Speech-to-Text) 웹 애플리케이션입니다. FastAPI 기반의 REST API를 제공하며, 변환된 텍스트를 파일로 저장할 수 있습니다.

## 🛠️ 주요 기능
- **Whisper STT 모델**을 이용한 음성 인식 (로컬 실행)
- **MP3, WAV 등 다양한 오디오 포맷 지원**
- **FastAPI 기반 웹 서버**
- **텍스트 파일(.txt)로 변환 결과 저장**
- **웹 UI 또는 API로 테스트 가능**

## 📂 폴더 구조
```
speech_to_text_project/
│── models/               # Whisper 모델 캐시 저장 폴더 (필요한 경우)
│── temp/                 # 업로드된 오디오 파일 및 변환된 텍스트 저장
│── whisper_stt.py        # STT 변환 메인 코드
│── requirements.txt      # 필수 패키지 목록
│── run_server.sh         # FastAPI 서버 실행 스크립트 (옵션)
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
```bash
uvicorn whisper_stt:app --host 0.0.0.0 --port 8000
```

### 4️⃣ **API 테스트 방법**
#### 📌 **Swagger UI 사용 (브라우저에서 테스트 가능)**
1. 서버 실행 후, **브라우저에서 아래 URL 접속**
   ```
   http://127.0.0.1:8000/docs
   ```
2. **`/stt/` 엔드포인트 선택 → "Try it out" 버튼 클릭 → 오디오 파일 업로드 → Execute 실행**
3. 변환된 텍스트 확인

#### 📌 **cURL 명령어로 테스트 (터미널 사용)**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/stt/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_audio_file.mp3'
```

#### 📌 **Postman을 사용한 테스트**
1. **Postman 실행**
2. **새 요청 생성** (`POST` 요청)
3. **URL 입력**:
   ```
   http://127.0.0.1:8000/stt/
   ```
4. **Body → form-data 선택**
   - Key: `file`
   - Value: 음성 파일 업로드
5. **Send 버튼 클릭** → 변환된 텍스트 확인

### 📄 **응답 예시 (JSON)**
```json
{
  "transcript": "안녕하세요, 이 테스트는 Whisper STT를 사용하여 음성을 텍스트로 변환하는 기능을 확인하는 것입니다.",
  "txt_file": "temp/your_audio_file.txt"
}
```

## 🛠️ 추가 기능 개발 예정
- 텍스트 전처리 (불필요한 단어 제거, 문장 정리)
- 요약 기능 추가 (추출 요약 & 추상 요약)
- 프론트엔드 UI 추가

---
📌 **문의 및 개선 사항은 언제든지 제안해 주세요! 🚀**

