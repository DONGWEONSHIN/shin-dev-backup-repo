"""RAG 질의응답 엔진을 제공하는 모듈입니다."""

from app.core.config import CHROMA_PERSIST_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL
from chromadb.errors import InvalidCollectionException
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

if OLLAMA_MODEL is None:
    raise ValueError("OLLAMA_MODEL 환경변수가 설정되어 있지 않습니다.")

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
    system=(
        """당신은 도움이 되는 AI 어시스턴트입니다. 모든 답변을 한국어로 해주세요.\n"
        "전문적이고 정중한 어투를 사용해주세요."""
    ),
)
embeddings = OllamaEmbeddings(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
)


def answer(question: str) -> dict:
    """질문에 대해 RAG 기반 답변과 출처를 반환합니다."""
    vectorstore = Chroma(
        collection_name="rag_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    try:
        search_results = vectorstore.similarity_search_with_score(question, k=5)
    except InvalidCollectionException:
        return {
            "answer": (
                "문서가 업로드/처리되지 않았거나, 벡터스토어가 비어 있습니다. "
                "PDF를 먼저 업로드하세요."
            ),
            "sources": [],
        }
    if not search_results:
        return {"answer": "관련 문서를 찾을 수 없습니다.", "sources": []}
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
    prompt = (
        f"아래 문서 내용을 참고하여 사용자의 질문에 답변하세요.\n\n[문서]\n{context_text}"
        f"\n\n[질문]\n{question}\n\n[답변]"
    )
    response = llm.invoke(prompt)
    content = response.content
    if isinstance(content, str):
        answer_text = content.strip()
    else:
        answer_text = str(content)
    if source_lines:
        answer_text += "\n\n[참고 문서]\n" + "\n".join(source_lines)
    return {"answer": answer_text, "sources": sources}


