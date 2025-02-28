# Python : 3.9.21
# Created: Feb. 28. 2025
# Updated: Feb. 28. 2025
# File: whisper_stt_v2.py
# Author: D.W. SHIN

import whisper
import os
import ffmpeg
import re
import nltk
import shutil
import torch
import uuid
import base64
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile, HTTPException
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import pipeline
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI()

# Whisper 모델 로드
MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
print(f"Using Whisper model: {MODEL_SIZE}")
model = whisper.load_model(MODEL_SIZE)

# Hugging Face 추상 요약 모델 로드
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", "facebook/bart-large-cnn")
print(f"Using summary model: {SUMMARY_MODEL}")
summary_pipeline = pipeline(
    "summarization", model=SUMMARY_MODEL, device=0 if torch.cuda.is_available() else -1
)


# 파일명 보호 함수
def secure_filename(filename):
    ext = filename.split(".")[-1]
    return f"{uuid.uuid4().hex}.{ext}"


# FFmpeg 실행 확인
def check_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise HTTPException(
            status_code=500, detail="FFmpeg 또는 ffprobe가 설치되지 않았습니다."
        )


check_ffmpeg()


# 파일 확장자 검증
def validate_audio_file(filename: str):
    if not filename.lower().endswith(("mp3", "wav", "m4a")):
        raise HTTPException(status_code=400, detail="지원되지 않는 파일 형식입니다.")


# 오디오 변환 (MP3 → WAV)
def convert_to_wav(input_file: str, output_file: str):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")


# STT 변환 함수
def transcribe_audio(file_path: str) -> str:
    try:
        result = model.transcribe(file_path)
        return result.get("text", "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT 변환 중 오류 발생: {str(e)}")


# 텍스트 전처리 (불필요한 단어 제거)
FILLER_WORDS = ["음", "어", "그러니까", "아", "에", "그", "자"]


def preprocess_text(text: str) -> str:
    pattern = r"\b(" + "|".join(map(re.escape, FILLER_WORDS)) + r")\b"
    text = re.sub(pattern, "", text)
    sentences = sent_tokenize(text)
    return " ".join(sentences).strip()


# 추출 요약 함수 (TextRank 사용)
def extractive_summary(text: str, sentence_count: int = 3) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("korean"))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary_sentences).strip()


# 추상 요약 함수 (BART 사용)
def abstractive_summary(text: str, max_length: int = 150, min_length: int = 50) -> str:
    summary = summary_pipeline(
        text, max_length=max_length, min_length=min_length, do_sample=False
    )
    return summary[0]["summary_text"]


# Base64 인코딩 함수
def encode_file_to_base64(filepath):
    with open(filepath, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# FastAPI 엔드포인트: 음성 → 텍스트 변환 및 요약 처리
@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    validate_audio_file(file.filename)
    os.makedirs("temp", exist_ok=True)

    # 안전한 파일명 생성
    secure_name = secure_filename(file.filename)
    file_path = os.path.join("temp", secure_name)

    # 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # WAV 변환 필요 시 변환
    wav_path = file_path
    if not file.filename.endswith(".wav"):
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        convert_to_wav(file_path, wav_path)

    # STT 실행
    transcript = transcribe_audio(wav_path)
    processed_text = preprocess_text(transcript)

    # 요약 수행
    extractive = extractive_summary(processed_text, 3)
    abstractive = abstractive_summary(processed_text)

    # 파일 저장
    text_path = wav_path.replace(".wav", "_transcript.txt")
    extractive_path = wav_path.replace(".wav", "_extractive_summary.txt")
    abstractive_path = wav_path.replace(".wav", "_abstractive_summary.txt")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(processed_text)
    with open(extractive_path, "w", encoding="utf-8") as f:
        f.write(extractive)
    with open(abstractive_path, "w", encoding="utf-8") as f:
        f.write(abstractive)

    return {
        "processed_text": processed_text,
        "extractive_summary": extractive,
        "abstractive_summary": abstractive,
        "files": {
            "transcript": encode_file_to_base64(text_path),
            "extractive_summary": encode_file_to_base64(extractive_path),
            "abstractive_summary": encode_file_to_base64(abstractive_path),
        },
    }
