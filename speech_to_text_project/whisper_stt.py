# Python : 3.9.21
# Created: Feb. 27. 2025
# Updated: Feb. 27. 2025
# Author: D.W. SHIN

import whisper
import os
import ffmpeg
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile
import shutil

# FastAPI 앱 생성
app = FastAPI()

# Whisper 모델 로드 (tiny, base, small, medium, large 중 선택 가능)
model = whisper.load_model("large")


# 오디오 변환 함수 (MP3 → WAV 등 지원)
def convert_to_wav(input_file: str, output_file: str):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")


# STT 변환 함수
def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result["text"]


# FastAPI 엔드포인트: 파일 업로드 & STT 변환
@app.post("/stt/")
async def upload_audio(file: UploadFile = File(...)):
    # 업로드된 파일 저장 경로
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # WAV 변환 필요 시 처리
    wav_path = file_path
    if not file.filename.endswith(".wav"):
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        convert_to_wav(file_path, wav_path)

    # STT 실행
    transcript = transcribe_audio(wav_path)

    # 변환된 텍스트를 TXT 파일로 저장
    txt_path = wav_path.replace(".wav", ".txt")
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(transcript)

    return {"transcript": transcript, "txt_file": txt_path}
