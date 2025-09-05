"""
데이터베이스 모델 패키지 초기화
모든 모델을 여기서 import하여 Alembic이 인식할 수 있도록 함
"""

# 베이스 모델
from app.db.base import Base

# 사용자 관련 모델
from app.db.models.user import User, UserPreference, UserRole, EmailFrequency

# 뉴스 관련 모델
from app.db.models.news import (
    NewsArticle,
    NewsSummary,
    NewsKeyword,
    NewsCategory,
    NewsStatus,
    SentimentType
)

# 이메일 관련 모델
from app.db.models.email import (
    EmailTemplate,
    EmailLog,
    EmailDigest,
    EmailStatus,
    EmailType
)

# 모든 모델을 하나의 리스트로 내보내기 (Alembic 자동 인식용)
__all__ = [
    "Base",
    # 사용자 모델
    "User",
    "UserPreference", 
    "UserRole",
    "EmailFrequency",
    # 뉴스 모델
    "NewsArticle",
    "NewsSummary",
    "NewsKeyword",
    "NewsCategory",
    "NewsStatus",
    "SentimentType",
    # 이메일 모델
    "EmailTemplate",
    "EmailLog",
    "EmailDigest",
    "EmailStatus",
    "EmailType",
]