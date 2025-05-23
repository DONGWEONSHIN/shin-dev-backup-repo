"""사용자 및 인증 관련 모델을 정의하는 모듈입니다."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

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


class Token(BaseModel):
    """토큰 모델입니다."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """토큰에 포함될 데이터 모델입니다."""

    email: Optional[str] = None
