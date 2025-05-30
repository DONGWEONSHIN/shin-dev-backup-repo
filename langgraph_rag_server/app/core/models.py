"""사용자 및 인증 관련 모델을 정의하는 모듈입니다."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from sqlalchemy import Boolean, Column, DateTime, String

from app.core.database import Base


# SQLAlchemy 모델
class UserDB(Base):
    """데이터베이스 사용자 모델입니다."""

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Pydantic 모델
class User(BaseModel):
    """사용자 모델입니다."""

    id: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """사용자 생성을 위한 모델입니다."""

    email: EmailStr
    password: str

    @classmethod
    def validate_password(cls, value: str) -> str:
        import re

        if len(value) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다.")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("비밀번호에는 영문자가 포함되어야 합니다.")
        if not re.search(r"[0-9]", value):
            raise ValueError("비밀번호에는 숫자가 포함되어야 합니다.")
        return value

    # Pydantic v2 field validator
    _validate_password = field_validator("password")(validate_password)


class Token(BaseModel):
    """토큰 모델입니다."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """토큰에 포함될 데이터 모델입니다."""

    email: Optional[str] = None
