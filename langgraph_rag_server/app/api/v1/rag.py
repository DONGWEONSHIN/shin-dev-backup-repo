"""RAG API 엔드포인트를 정의하는 모듈입니다."""

from typing import Any, Dict

from app.core import rag_engine
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    """질문 요청을 위한 데이터 모델입니다."""

    question: str


@router.post("/query")
def rag_query(request: QueryRequest) -> Dict[str, Any]:
    """질문에 대해 RAG 기반 답변을 반환합니다."""
    answer = rag_engine.answer(request.question)
    # 벡터스토어가 비어있거나 collection이 없을 때 안내 메시지 반환
    if answer["answer"].startswith("문서가 업로드/처리되지 않았거나") or answer[
        "answer"
    ].startswith("관련 문서를 찾을 수 없습니다"):
        return {
            "answer": "문서가 없습니다. PDF를 먼저 업로드하고 처리하세요.",
            "sources": [],
        }
    return answer
