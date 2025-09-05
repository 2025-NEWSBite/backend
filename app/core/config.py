"""
애플리케이션 설정 관리
환경 변수를 통한 설정값 로드 및 검증
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseSettings, validator, EmailStr, PostgresDsn


class Settings(BaseSettings):
    """
    애플리케이션 전체 설정
    환경 변수 또는 .env 파일에서 값을 로드
    """
    
    # 기본 앱 정보
    PROJECT_NAME: str = "NewsBite API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "뉴스한입 - 개인맞춤 뉴스 요약 서비스 API"
    DEBUG: bool = True
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql+asyncpg://newsbite_user:newsbite_password@db:5432/newsbite"
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        """데이터베이스 URL 유효성 검증"""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=v.get("user"),
            password=v.get("password"),
            host=v.get("host"),
            port=v.get("port"),
            path=f"/{v.get('path') or ''}",
        )
    
    # Redis 설정
    REDIS_URL: str = "redis://redis:6379"
    REDIS_TTL: int = 3600  # 1시간
    
    # JWT 토큰 설정
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1시간
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7     # 7일
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://frontend:3000"
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """CORS 오리진 설정 파싱"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Firebase 설정 (구글 로그인)
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_PRIVATE_KEY_ID: Optional[str] = None
    FIREBASE_PRIVATE_KEY: Optional[str] = None
    FIREBASE_CLIENT_EMAIL: Optional[str] = None
    FIREBASE_CLIENT_ID: Optional[str] = None
    
    # 이메일 발송 설정
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[EmailStr] = None
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "뉴스한입 NewsBite"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    
    # AI 모델 설정
    HUGGINGFACE_API_TOKEN: Optional[str] = None
    SUMMARIZATION_MODEL: str = "facebook/bart-large-cnn"
    CLASSIFICATION_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    
    # AWS 설정 (이미지 업로드)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-northeast-2"
    AWS_S3_BUCKET: Optional[str] = None
    
    # 뉴스 크롤링 설정
    NAVER_NEWS_API_KEY: Optional[str] = None
    NAVER_NEWS_SECRET_KEY: Optional[str] = None
    NEWS_CRAWL_INTERVAL: int = 30  # 30분마다
    MAX_NEWS_PER_CATEGORY: int = 50
    
    # OpenAI 설정
    OPENAI_API_KEY: Optional[str] = None
    
    # Celery 설정 (비동기 작업)
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "{time} | {level} | {name} | {message}"
    
    # API 제한 설정
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # 파일 업로드 설정
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    
    # 페이지네이션 기본값
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()