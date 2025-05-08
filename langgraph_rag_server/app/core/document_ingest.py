"""PDF 문서 임베딩 및 벡터스토어 저장 기능을 제공하는 모듈입니다."""

import os
import shutil

from app.core.config import CHROMA_PERSIST_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def ingest_documents(documents_dir: str | None = None) -> str:
    """PDF 문서를 임베딩하고 벡터스토어에 저장합니다."""
    if not OLLAMA_MODEL:
        return "OLLAMA_MODEL 환경변수가 설정되어 있지 않습니다."

    # 임베딩 및 벡터스토어 초기화
    embeddings = OllamaEmbeddings(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
    )
    # PDF 파일 수집
    pdf_files = []
    for root, _, files in os.walk(documents_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    if not pdf_files:
        return "PDF 문서가 없습니다."

    # 문서 로딩 및 청크 분할
    all_splits = []
    for file_path in pdf_files:
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            enhanced_docs = []
            for doc in documents:
                doc.page_content = " ".join(doc.page_content.split())
                if not doc.page_content.strip():
                    continue
                doc.metadata["source"] = file_path
                doc.metadata["filename"] = os.path.basename(file_path)
                doc.metadata["char_count"] = len(doc.page_content)
                doc.metadata["word_count"] = len(doc.page_content.split())
                enhanced_docs.append(doc)
            splits = text_splitter.split_documents(enhanced_docs)
            all_splits.extend(splits)
        except Exception as e:  # noqa: E722
            return f"{file_path} 처리 중 오류: {str(e)}"

    if not all_splits:
        return "유효한 문서 내용이 추출되지 않았습니다."

    # 벡터스토어 초기화 및 저장
    vectorstore = Chroma(
        collection_name="rag_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    vectorstore.delete_collection()
    vectorstore = Chroma(
        collection_name="rag_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    batch_size = 50
    for i in range(0, len(all_splits), batch_size):
        batch = all_splits[i : i + batch_size]
        vectorstore.add_documents(batch)
    return f"총 {len(all_splits)}개의 문서 청크가 벡터스토어에 저장되었습니다."


def delete_related_chroma_files(filename: str):
    """ChromaDB 데이터 폴더에서 filename 관련 벡터 파일 삭제."""
    for folder in os.listdir(CHROMA_PERSIST_DIR):
        folder_path = os.path.join(CHROMA_PERSIST_DIR, folder)
        if os.path.isdir(folder_path):
            # 메타데이터 파일 탐색
            metadata_file = os.path.join(folder_path, "metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    content = f.read()
                    if filename in content:
                        # 관련 UUID 폴더 삭제
                        shutil.rmtree(folder_path)
                        print(f"✅ {folder_path} 관련 데이터 삭제 완료")
