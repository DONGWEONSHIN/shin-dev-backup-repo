"""사용자 및 인증 관련 모델을 정의하는 모듈입니다."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """사용자 모델입니다."""

    id: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class UserCreate(BaseModel):
    """사용자 생성을 위한 모델입니다."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT 토큰 모델입니다."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰에 포함될 데이터 모델입니다."""

    email: Optional[str] = None
