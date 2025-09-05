"""
보안 관련 유틸리티
비밀번호 해싱, JWT 토큰 생성/검증 등
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    액세스 토큰 생성
    
    Args:
        subject: 토큰 subject (보통 사용자 ID)
        expires_delta: 토큰 만료 시간 (선택사항)
    
    Returns:
        str: JWT 액세스 토큰
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    리프레시 토큰 생성
    
    Args:
        subject: 토큰 subject (보통 사용자 ID)
        expires_delta: 토큰 만료 시간 (선택사항)
    
    Returns:
        str: JWT 리프레시 토큰
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    JWT 토큰 검증
    
    Args:
        token: 검증할 JWT 토큰
        token_type: 토큰 타입 ("access" 또는 "refresh")
    
    Returns:
        Optional[str]: 토큰이 유효하면 subject, 그렇지 않으면 None
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_sub: str = payload.get("sub")
        token_type_payload: str = payload.get("type")
        
        if token_sub is None or token_type_payload != token_type:
            return None
            
        return token_sub
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 검증
    
    Args:
        plain_password: 평문 비밀번호
        hashed_password: 해시된 비밀번호
    
    Returns:
        bool: 비밀번호가 일치하면 True, 그렇지 않으면 False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    비밀번호 해시 생성
    
    Args:
        password: 평문 비밀번호
    
    Returns:
        str: 해시된 비밀번호
    """
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    """
    비밀번호 재설정 토큰 생성
    
    Args:
        email: 사용자 이메일
    
    Returns:
        str: 비밀번호 재설정 토큰
    """
    delta = timedelta(hours=1)  # 1시간 유효
    now = datetime.utcnow()
    expires = now + delta
    
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "password_reset"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    비밀번호 재설정 토큰 검증
    
    Args:
        token: 재설정 토큰
    
    Returns:
        Optional[str]: 토큰이 유효하면 이메일, 그렇지 않으면 None
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_type: str = decoded_token.get("type")
        if token_type != "password_reset":
            return None
        return decoded_token["sub"]
    except JWTError:
        return None


def generate_email_verification_token(email: str) -> str:
    """
    이메일 인증 토큰 생성
    
    Args:
        email: 사용자 이메일
    
    Returns:
        str: 이메일 인증 토큰
    """
    delta = timedelta(hours=24)  # 24시간 유효
    now = datetime.utcnow()
    expires = now + delta
    
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "email_verification"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_email_verification_token(token: str) -> Optional[str]:
    """
    이메일 인증 토큰 검증
    
    Args:
        token: 인증 토큰
    
    Returns:
        Optional[str]: 토큰이 유효하면 이메일, 그렇지 않으면 None
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_type: str = decoded_token.get("type")
        if token_type != "email_verification":
            return None
        return decoded_token["sub"]
    except JWTError:
        return None