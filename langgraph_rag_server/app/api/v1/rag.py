"""RAG API 엔드포인트를 정의하는 모듈입니다."""

from typing import Any, Dict, Optional

from app.core import rag_engine
from app.core.auth import get_current_user
from app.core.models import User
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


class QueryRequest(BaseModel):
    """질문 요청을 위한 데이터 모델입니다."""

    question: str


async def get_current_user_api(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """API에서 사용할 인증 미들웨어입니다. 토큰 또는 쿠키에서 사용자 정보를 가져옵니다."""
    # 헤더의 토큰 먼저 확인
    if token:
        return await get_current_user(token, db)

    # Authorization 헤더 직접 확인
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        try:
            return await get_current_user(token, db)
        except Exception:
            pass

    # 쿠키에서 토큰 확인
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return await get_current_user(cookie_token, db)

    # 둘 다 없으면 인증 실패
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/query")
async def rag_query(
    request: Request, query_request: QueryRequest, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """질문에 대해 RAG 기반 답변을 반환합니다."""
    # 입력값 검증: 길이 제한 및 공백만 입력 방지
    q = query_request.question
    if not (1 <= len(q.strip()) <= 300):
        raise HTTPException(
            status_code=400,
            detail=(
                "질문은 1~300자 이내로 입력해야 하며, " "공백만 입력할 수 없습니다."
            ),
        )
    current_user = await get_current_user_api(request, None, db)
    answer = rag_engine.answer(q, current_user.id)
    # 벡터스토어가 비어있거나 collection이 없을 때 안내 메시지 반환
    if answer["answer"].startswith("문서가 업로드/처리되지 않았거나") or answer[
        "answer"
    ].startswith("관련 문서를 찾을 수 없습니다"):
        return {
            "answer": "문서가 없습니다. PDF를 먼저 업로드하고 처리하세요.",
            "sources": [],
        }
    return answer
