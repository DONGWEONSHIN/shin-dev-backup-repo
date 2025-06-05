"""RAG 질의응답 엔진을 제공하는 모듈입니다."""

from app.core.config import (
    CHROMA_PERSIST_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_LLM_MODEL,
    OLLAMA_EMBEDDING_MODEL,
)
from chromadb.errors import InvalidCollectionException
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
import logging
from functools import lru_cache
import hashlib

# 에러 메시지 상수
ERR_NO_MODEL = "OLLAMA_LLM_MODEL 환경변수가 설정되어 있지 않습니다."
ERR_NO_EMBED = "OLLAMA_EMBEDDING_MODEL 환경변수가 설정되어 있지 않습니다."
ERR_VECTORSTORE = "문서가 업로드/처리되지 않았거나, 벡터스토어가 비어 있습니다. PDF를 먼저 업로드하세요."
ERR_NO_DOCS = "관련 문서를 찾을 수 없습니다."
ERR_LLM = "LLM 호출 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
ERR_UNKNOWN = "알 수 없는 오류가 발생했습니다. 관리자에게 문의하세요."

# 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if OLLAMA_LLM_MODEL is None:
    logger.error(ERR_NO_MODEL)
    raise ValueError(ERR_NO_MODEL)
if OLLAMA_EMBEDDING_MODEL is None:
    logger.error(ERR_NO_EMBED)
    raise ValueError(ERR_NO_EMBED)

llm = ChatOllama(
    model=OLLAMA_LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
    system=(
        """당신은 도움이 되는 AI 어시스턴트입니다. 모든 답변을 한국어로 해주세요.\n"
        "전문적이고 정중한 어투를 사용해주세요."""
    ),
)
embeddings = OllamaEmbeddings(
    model=OLLAMA_EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL,
)


def get_user_collection_name(user_id: str) -> str:
    """사용자별 컬렉션 이름을 반환합니다."""
    return f"rag_docs_{user_id}"


# 질문+context_text 조합에 대해 LLM 응답을 캐싱
@lru_cache(maxsize=128)
def cached_llm_response(prompt_hash: str, prompt: str):
    response = llm.invoke(prompt)
    content = response.content
    if isinstance(content, str):
        return content.strip()
    return str(content)


def answer(question: str, user_id: str, thinking_mode: bool = True) -> dict:
    """질문에 대해 RAG 기반 답변과 출처, (옵션)추론을 반환합니다."""
    collection_name = get_user_collection_name(user_id)
    try:
        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR,
        )
        try:
            search_results = vectorstore.similarity_search_with_score(question, k=8)
            logger.info(f"[RAG] 검색된 문서 청크 개수: {len(search_results)}")
            for idx, (doc, score) in enumerate(search_results):
                logger.debug(
                    f"[청크 {idx+1}] (유사도 점수: {score:.4f}) 파일: "
                    f"{doc.metadata.get('filename', 'unknown')} "
                    f"페이지: {doc.metadata.get('page', 'unknown')}"
                )
        except InvalidCollectionException:
            logger.warning(f"[RAG] 벡터스토어 컬렉션 없음: {collection_name}")
            return {"answer": ERR_VECTORSTORE, "sources": []}
        except Exception as e:
            logger.error(f"[RAG] 벡터스토어 검색 오류: {e}")
            return {"answer": ERR_UNKNOWN, "sources": []}
        if not search_results:
            return {"answer": ERR_NO_DOCS, "sources": []}
        context_chunks = []
        sources = []
        source_lines = []
        for idx, (doc, score) in enumerate(search_results):
            context_chunks.append(doc.page_content)
            src = {
                "filename": doc.metadata.get("filename", "unknown"),
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "unknown"),
                "score": float(score),
                "preview": doc.page_content[:100],
            }
            sources.append(src)
            rel = "높음" if idx < 3 else "중간"
            source_lines.append(
                f"- {src['filename']} (페이지: {src['page']}, 관련도: {rel})"
            )
        context_text = "\n---\n".join(context_chunks)
        # 프롬프트 본문은 추론/비추론 모두 완전히 동일하게 작성
        prompt = (
            f"아래 문서 내용을 참고하여 사용자의 질문에 답변하세요.\n"
            f"[문서]\n{context_text}\n"
            f"[질문]\n{question}\n"
            f"[답변] 아래에 답변을 작성하세요.\n"
            f"[답변]"
        )
        if not thinking_mode:
            prompt += "\n/no_think"
        try:
            prompt_hash = hashlib.sha256((question + context_text + str(thinking_mode)).encode("utf-8")).hexdigest()
            answer_text = cached_llm_response(prompt_hash, prompt)
            logger.info(f"[LLM 응답 원문] {answer_text}")
            # <think>...</think> 태그가 있으면 그 안의 내용을 think, 이후 내용을 answer로 분리. 없으면 전체를 answer로, think는 빈 문자열.
            import re
            answer_part = ""
            think_part = ""
            m3 = re.search(r"<think>(.*?)</think>(.*)", answer_text, re.DOTALL)
            if m3:
                think_part = m3.group(1).strip()
                answer_part = m3.group(2).strip()
            else:
                answer_part = answer_text.strip()
            # 참고 문서 정보 추가
            if source_lines:
                answer_part += "\n\n[참고 문서]\n" + "\n".join(source_lines)
            return {"answer": answer_part, "think": think_part, "sources": sources}
        except Exception as e:
            logger.error(f"[RAG] LLM 호출 오류: {e}")
            return {"answer": ERR_LLM, "sources": sources}
    except Exception as e:
        logger.critical(f"[RAG] 알 수 없는 오류: {e}")
        return {"answer": ERR_UNKNOWN, "sources": []}
