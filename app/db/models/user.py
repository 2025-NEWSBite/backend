"""
사용자 관련 데이터베이스 모델
"""

from sqlalchemy import Boolean, Column, String, Text, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base import Base, TimestampMixin, UUIDMixin


class UserRole(str, Enum):
    """사용자 권한 enum"""
    ADMIN = "admin"      # 관리자
    USER = "user"        # 일반 사용자
    PREMIUM = "premium"  # 프리미엄 사용자


class EmailFrequency(str, Enum):
    """이메일 발송 주기 enum"""
    DAILY = "daily"          # 매일
    WEEKLY = "weekly"        # 주간
    MONTHLY = "monthly"      # 월간
    DISABLED = "disabled"    # 비활성화


class User(Base, UUIDMixin, TimestampMixin):
    """
    사용자 모델
    인증, 개인정보, 설정 정보를 관리
    """
    __tablename__ = "users"

    # 기본 정보
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="이메일 주소"
    )
    password_hash = Column(
        String(255),
        nullable=True,  # 소셜 로그인 사용자는 비밀번호가 없을 수 있음
        comment="해시된 비밀번호"
    )
    full_name = Column(
        String(100),
        nullable=False,
        comment="사용자 이름"
    )
    
    # 계정 상태
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="계정 활성화 상태"
    )
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="이메일 인증 상태"
    )
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False,
        comment="사용자 권한"
    )
    
    # 프로필 정보
    profile_image = Column(
        String(500),
        nullable=True,
        comment="프로필 이미지 URL"
    )
    bio = Column(
        Text,
        nullable=True,
        comment="자기소개"
    )
    
    # 이메일 설정
    email_frequency = Column(
        SQLEnum(EmailFrequency),
        default=EmailFrequency.DAILY,
        nullable=False,
        comment="이메일 발송 주기"
    )
    email_time_hour = Column(
        Integer,
        default=9,  # 오전 9시
        nullable=False,
        comment="이메일 발송 시간 (시)"
    )
    
    # 소셜 로그인 정보
    google_id = Column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
        comment="구글 소셜 로그인 ID"
    )
    
    # 관계 설정
    preferences = relationship(
        "UserPreference",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False
    )
    
    def __repr__(self) -> str:
        return f"<User(email='{self.email}', full_name='{self.full_name}')>"


class UserPreference(Base, UUIDMixin, TimestampMixin):
    """
    사용자 개인화 설정
    뉴스 카테고리 선호도 및 기타 설정
    """
    __tablename__ = "user_preferences"
    
    # 외래키
    user_id = Column(
        "user_id",
        UUIDMixin.id.type,
        # ForeignKey("users.id"),
        nullable=False,
        comment="사용자 ID"
    )
    
    # 뉴스 카테고리 선호도 (JSON으로 저장)
    preferred_categories = Column(
        Text,  # JSON 형태로 저장: ["politics", "economy", "society"]
        nullable=True,
        comment="선호 뉴스 카테고리 (JSON 배열)"
    )
    
    # 요약 설정
    summary_length = Column(
        SQLEnum("short", "medium", "long", name="summary_length_enum"),
        default="medium",
        nullable=False,
        comment="요약 길이 설정"
    )
    
    # 언어 설정
    language = Column(
        String(10),
        default="ko",
        nullable=False,
        comment="언어 설정"
    )
    
    # 알림 설정
    push_notification = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="푸시 알림 활성화"
    )
    email_notification = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="이메일 알림 활성화"
    )
    
    # 관계 설정
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self) -> str:
        return f"<UserPreference(user_id='{self.user_id}')>"