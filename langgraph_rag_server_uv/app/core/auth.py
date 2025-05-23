"""인증 관련 유틸리티 함수를 제공하는 모듈입니다."""

import os
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.core.database import get_db
from app.core.models import TokenData, User, UserDB

# .env 파일 로드
load_dotenv()

# 설정
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")  # 기본값 설정
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# CryptContext 설정 수정
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # bcrypt 라운드 수 설정
    bcrypt__ident="2b",  # bcrypt 식별자 설정
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호를 검증합니다."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호를 해시화합니다."""
    return pwd_context.hash(password)


def get_user(db: Session, email: str) -> Optional[User]:
    """이메일로 사용자를 조회합니다."""
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if user:
        return User.model_validate(user)
    return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """사용자 인증을 수행합니다."""
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰을 생성합니다."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """현재 인증된 사용자를 반환합니다."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def create_new_user(db: Session, email: EmailStr, password: str) -> User:
    """새 사용자를 생성합니다."""
    # 이메일 중복 확인
    if get_user(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 새 사용자 생성
    hashed_password = get_password_hash(password)
    db_user = UserDB(
        id=str(uuid4()),
        email=email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)
