# Python : 3.9.21
# Created: Feb. 27. 2025
# Updated: Feb. 28. 2025
# Author: D.W. SHIN

import whisper
import os
import ffmpeg
import re
import nltk
import shutil
import torch
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile, HTTPException
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import pipeline

# NLTK punkt 다운로드 (경로 지정 없이 기본값 사용)
nltk.download("punkt", quiet=True)

# FastAPI 앱 생성
app = FastAPI()

# Whisper 모델 로드 (tiny, base, small, medium, large 중 선택 가능)
MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
model = whisper.load_model(MODEL_SIZE)

# Hugging Face 추상 요약 모델 로드
SUMMARY_MODEL = "facebook/bart-large-cnn"
summary_pipeline = pipeline(
    "summarization", model=SUMMARY_MODEL, device=0 if torch.cuda.is_available() else -1
)


# FFmpeg 실행 가능 여부 확인 함수
def check_ffmpeg():
    """FFmpeg 및 ffprobe 실행 가능 여부 확인"""
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")

    if not ffmpeg_path or not ffprobe_path:
        raise HTTPException(
            status_code=500,
            detail=f"FFmpeg 또는 ffprobe가 설치되지 않았거나 찾을 수 없습니다. "
            f"(ffmpeg: {ffmpeg_path}, ffprobe: {ffprobe_path})",
        )

    try:
        # `ffmpeg.probe()`를 실행 파일이 아닌 실제 오디오 파일로 실행
        test_audio = "/usr/share/sounds/alsa/Front_Center.wav"  # 시스템 내 기본 오디오 파일 (Ubuntu 기본 제공)
        ffmpeg.probe(test_audio)
    except ffmpeg.Error as e:
        stderr_output = e.stderr.decode() if hasattr(e, "stderr") else str(e)
        raise HTTPException(
            status_code=500, detail=f"FFmpeg 실행 중 오류 발생:\n{stderr_output}"
        )


check_ffmpeg()


# 파일 확장자 검증 함수 (MP3, WAV, M4A 지원)
def validate_audio_file(filename: str):
    if not filename.lower().endswith(("mp3", "wav", "m4a")):
        raise HTTPException(
            status_code=400,
            detail=f"지원되지 않는 파일 형식입니다: {filename.split('.')[-1]}",
        )


# 오디오 변환 함수 (MP3 → WAV 등 지원)
def convert_to_wav(input_file: str, output_file: str):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")


# STT 변환 함수
def transcribe_audio(file_path: str) -> str:
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT 변환 중 오류 발생: {str(e)}")


# 텍스트 전처리 함수 (문장 분리 및 불필요한 단어 제거)
def preprocess_text(text: str) -> str:
    # 불필요한 단어 제거
    text = re.sub(r"\b(음|어|그러니까|음...|아|에|그|자|어...)\b", "", text)
    try:
        # 문장 분리
        sentences = sent_tokenize(text)
        # 공백 정리 및 재구성
        cleaned_text = " ".join(sentences)
        return cleaned_text.strip()
    except LookupError:
        nltk.download("punkt", quiet=True)
        return " ".join(sent_tokenize(text)).strip()


# 추출 요약 함수 (TextRank 사용)
def extractive_summary(text: str, sentence_count: int = 3) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("korean"))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count)
    summary = " ".join(str(sentence) for sentence in summary_sentences)
    return summary.strip()


# 추상 요약 함수 (BART 사용)
def abstractive_summary(text: str, max_length: int = 150, min_length: int = 50) -> str:
    summary = summary_pipeline(
        text, max_length=max_length, min_length=min_length, do_sample=False
    )
    return summary[0]["summary_text"]


# FastAPI 엔드포인트: 파일 업로드 & STT 변환
@app.post("/stt/")
async def upload_audio(file: UploadFile = File(...)):
    validate_audio_file(file.filename)

    # 업로드된 파일 저장 경로
    os.makedirs("temp", exist_ok=True)  # temp 폴더 자동 생성
    file_path = f"temp/{file.filename}"

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

    # 텍스트 전처리 실행
    processed_text = preprocess_text(transcript)

    # 변환된 텍스트를 TXT 파일로 저장
    txt_path = wav_path.replace(".wav", "_processed.txt")
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(processed_text)

    return {"processed_text": processed_text, "txt_file": txt_path}


# FastAPI 엔드포인트: 추출 요약 (TextRank 기반)
@app.post("/summarize/extractive/")
async def summarize_extractive(text: str, sentence_count: int = 3):
    summary = extractive_summary(text, sentence_count)
    return {"summary": summary}


# FastAPI 엔드포인트: 파일 업로드 후 요약
@app.post("/summarize/extractive/file/")
async def summarize_file(file: UploadFile = File(...), sentence_count: int = 3):
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="지원되지 않는 파일 형식입니다. .txt 파일만 업로드하세요.",
        )

    # 파일 저장 경로
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 파일 내용 읽기
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 요약 수행
    summary = extractive_summary(text, sentence_count)

    # 요약된 내용을 파일로 저장
    summary_path = file_path.replace(".txt", "_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as summary_file:
        summary_file.write(summary)

    return {"summary": summary, "txt_file": summary_path}


# FastAPI 엔드포인트: 추상 요약 (BART 기반)
@app.post("/summarize/abstractive/")
async def summarize_abstractive(text: str, max_length: int = 150, min_length: int = 50):
    summary = abstractive_summary(text, max_length, min_length)
    return {"summary": summary}


# FastAPI 엔드포인트: 파일 업로드 후 추상 요약 수행
@app.post("/summarize/abstractive/file/")
async def summarize_abstractive_file(
    file: UploadFile = File(...), max_length: int = 150, min_length: int = 50
):
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="지원되지 않는 파일 형식입니다. .txt 파일만 업로드하세요.",
        )

    # 파일 저장 경로
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 파일 내용 읽기
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 요약 수행
    summary = abstractive_summary(text, max_length, min_length)

    # 요약된 내용을 파일로 저장
    summary_path = file_path.replace(".txt", "_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as summary_file:
        summary_file.write(summary)

    return {"summary": summary, "txt_file": summary_path}
