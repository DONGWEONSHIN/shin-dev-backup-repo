"""폴더 경로 및 설정 상수를 중앙집중식으로 정의하는 모듈입니다."""

import os
import shutil

from dotenv import load_dotenv

load_dotenv()


# 프로젝트 루트 경로 계산 (config.py에서 두 번 상위로)
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "../../../"))

# 폴더 경로 상수 정의
CHROMA_PERSIST_DIR = os.path.join(PROJECT_ROOT, "data", "chroma_db")
DOCUMENTS_DIR = os.path.join(PROJECT_ROOT, "data", "documents")
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "app", "templates")

FOLDER_PATHS = [CHROMA_PERSIST_DIR, DOCUMENTS_DIR, STATIC_DIR, TEMPLATES_DIR]
FOLDER_CLEAR = [CHROMA_PERSIST_DIR, DOCUMENTS_DIR]

print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"CHROMA_PERSIST_DIR: {CHROMA_PERSIST_DIR}")
print(f"DOCUMENTS_DIR: {DOCUMENTS_DIR}")
print(f"STATIC_DIR: {STATIC_DIR}")
print(f"TEMPLATES_DIR: {TEMPLATES_DIR}")


def ensure_directories():
    """필요한 폴더가 없으면 생성합니다."""
    for folder in FOLDER_PATHS:
        os.makedirs(folder, exist_ok=True)


def clear_directories():
    """지정된 폴더의 모든 파일과 하위 폴더를 삭제합니다."""
    for folder in FOLDER_CLEAR:
        if os.path.exists(folder):
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            print(f"{folder} 내부 파일이 모두 삭제되었습니다.")
        else:
            print(f"폴더가 존재하지 않습니다: {folder}")

# OLLAMA 관련 환경변수
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
