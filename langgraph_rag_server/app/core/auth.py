"""인증 관련 유틸리티 함수를 제공하는 모듈입니다."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core.models import TokenData, User

# 설정
SECRET_KEY = "your-secret-key"  # 실제 운영 환경에서는 환경 변수로 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# 임시 사용자 DB (실제 구현에서는 데이터베이스 사용)
fake_users_db = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호를 검증합니다."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호를 해시화합니다."""
    return pwd_context.hash(password)


def get_user(email: str) -> Optional[User]:
    """이메일로 사용자를 조회합니다."""
    if email in fake_users_db:
        user_dict = fake_users_db[email]
        return User(**user_dict)
    return None


def authenticate_user(email: str, password: str) -> Optional[User]:
    """사용자 인증을 수행합니다."""
    user = get_user(email)
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


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
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
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def create_new_user(email: EmailStr, password: str) -> User:
    """새 사용자를 생성합니다."""
    if email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(password)
    user = User(
        id=str(len(fake_users_db) + 1),
        email=email,
        hashed_password=hashed_password,
    )
    fake_users_db[email] = user.model_dump()
    return user
