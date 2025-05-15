"""RAG API 엔드포인트를 정의하는 모듈입니다."""

from typing import Any, Dict, Optional

from app.core import rag_engine
from app.core.auth import get_current_user
from app.core.models import User
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


class QueryRequest(BaseModel):
    """질문 요청을 위한 데이터 모델입니다."""

    question: str


async def get_current_user_api(
    request: Request, token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    """API에서 사용할 인증 미들웨어입니다. 토큰 또는 쿠키에서 사용자 정보를 가져옵니다."""
    # 헤더의 토큰 먼저 확인
    if token:
        return await get_current_user(token)

    # Authorization 헤더 직접 확인
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        try:
            return await get_current_user(token)
        except Exception:
            pass

    # 쿠키에서 토큰 확인
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return await get_current_user(cookie_token)

    # 둘 다 없으면 인증 실패
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/query")
async def rag_query(request: Request, query_request: QueryRequest) -> Dict[str, Any]:
    """질문에 대해 RAG 기반 답변을 반환합니다."""
    current_user = await get_current_user_api(request, None)
    answer = rag_engine.answer(query_request.question, current_user.id)
    # 벡터스토어가 비어있거나 collection이 없을 때 안내 메시지 반환
    if answer["answer"].startswith("문서가 업로드/처리되지 않았거나") or answer[
        "answer"
    ].startswith("관련 문서를 찾을 수 없습니다"):
        return {
            "answer": "문서가 없습니다. PDF를 먼저 업로드하고 처리하세요.",
            "sources": [],
        }
    return answer
