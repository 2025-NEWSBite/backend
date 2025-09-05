"""
이메일 발송 관련 데이터베이스 모델
"""

from sqlalchemy import Boolean, Column, String, Text, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime
from app.db.base import Base, TimestampMixin, UUIDMixin


class EmailStatus(str, Enum):
    """이메일 발송 상태 enum"""
    PENDING = "pending"      # 발송 대기
    PROCESSING = "processing"  # 처리 중
    SENT = "sent"           # 발송 완료
    FAILED = "failed"       # 발송 실패
    BOUNCED = "bounced"     # 반송됨
    OPENED = "opened"       # 읽음
    CLICKED = "clicked"     # 클릭함


class EmailType(str, Enum):
    """이메일 유형 enum"""
    DAILY_DIGEST = "daily_digest"      # 일간 뉴스 다이제스트
    WEEKLY_DIGEST = "weekly_digest"    # 주간 뉴스 다이제스트
    MONTHLY_DIGEST = "monthly_digest"  # 월간 뉴스 다이제스트
    BREAKING_NEWS = "breaking_news"    # 속보
    WELCOME = "welcome"                # 환영 메일
    VERIFICATION = "verification"      # 인증 메일
    PASSWORD_RESET = "password_reset"  # 비밀번호 재설정
    NOTIFICATION = "notification"      # 일반 알림


class EmailTemplate(Base, UUIDMixin, TimestampMixin):
    """
    이메일 템플릿 모델
    다양한 이메일 유형별 템플릿 관리
    """
    __tablename__ = "email_templates"

    # 템플릿 정보
    name = Column(
        String(100),
        unique=True,
        nullable=False,
        comment="템플릿 이름"
    )
    email_type = Column(
        SQLEnum(EmailType),
        nullable=False,
        comment="이메일 유형"
    )
    
    # 템플릿 내용
    subject_template = Column(
        String(200),
        nullable=False,
        comment="제목 템플릿"
    )
    html_template = Column(
        Text,
        nullable=False,
        comment="HTML 템플릿"
    )
    text_template = Column(
        Text,
        nullable=True,
        comment="텍스트 템플릿"
    )
    
    # 템플릿 설정
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="템플릿 활성화 상태"
    )
    version = Column(
        String(20),
        default="1.0",
        nullable=False,
        comment="템플릿 버전"
    )
    
    # 다국어 지원
    language = Column(
        String(10),
        default="ko",
        nullable=False,
        comment="템플릿 언어"
    )
    
    def __repr__(self) -> str:
        return f"<EmailTemplate(name='{self.name}', type='{self.email_type}')>"


class EmailLog(Base, UUIDMixin, TimestampMixin):
    """
    이메일 발송 로그 모델
    모든 이메일 발송 내역 추적
    """
    __tablename__ = "email_logs"

    # 수신자 정보
    user_id = Column(
        "user_id",
        UUIDMixin.id.type,
        # ForeignKey("users.id"),
        nullable=True,
        comment="수신 사용자 ID (회원인 경우)"
    )
    recipient_email = Column(
        String(255),
        nullable=False,
        index=True,
        comment="수신자 이메일 주소"
    )
    recipient_name = Column(
        String(100),
        nullable=True,
        comment="수신자 이름"
    )
    
    # 이메일 내용
    email_type = Column(
        SQLEnum(EmailType),
        nullable=False,
        comment="이메일 유형"
    )
    subject = Column(
        String(200),
        nullable=False,
        comment="이메일 제목"
    )
    html_content = Column(
        Text,
        nullable=True,
        comment="HTML 내용"
    )
    text_content = Column(
        Text,
        nullable=True,
        comment="텍스트 내용"
    )
    
    # 발송 정보
    status = Column(
        SQLEnum(EmailStatus),
        default=EmailStatus.PENDING,
        nullable=False,
        comment="발송 상태"
    )
    sent_at = Column(
        DateTime,
        nullable=True,
        comment="발송 시간"
    )
    
    # 추적 정보
    opened_at = Column(
        DateTime,
        nullable=True,
        comment="읽은 시간"
    )
    clicked_at = Column(
        DateTime,
        nullable=True,
        comment="클릭한 시간"
    )
    bounce_reason = Column(
        String(500),
        nullable=True,
        comment="반송 사유"
    )
    
    # 기술 정보
    message_id = Column(
        String(255),
        nullable=True,
        unique=True,
        comment="메시지 ID (SMTP)"
    )
    provider_response = Column(
        Text,
        nullable=True,
        comment="이메일 제공자 응답"
    )
    
    # 재시도 정보
    retry_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="재시도 횟수"
    )
    last_error = Column(
        Text,
        nullable=True,
        comment="마지막 에러 메시지"
    )
    
    def __repr__(self) -> str:
        return f"<EmailLog(recipient='{self.recipient_email}', type='{self.email_type}', status='{self.status}')>"


class EmailDigest(Base, UUIDMixin, TimestampMixin):
    """
    이메일 다이제스트 모델
    발송된 뉴스 다이제스트 정보 저장
    """
    __tablename__ = "email_digests"

    # 다이제스트 정보
    digest_date = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="다이제스트 날짜"
    )
    digest_type = Column(
        SQLEnum("daily", "weekly", "monthly", name="digest_type_enum"),
        nullable=False,
        comment="다이제스트 유형"
    )
    
    # 내용 정보
    title = Column(
        String(200),
        nullable=False,
        comment="다이제스트 제목"
    )
    summary = Column(
        Text,
        nullable=True,
        comment="전체 요약"
    )
    
    # 포함된 뉴스 기사들 (JSON)
    article_ids = Column(
        Text,  # JSON 배열로 저장
        nullable=True,
        comment="포함된 기사 ID들 (JSON 배열)"
    )
    
    # 통계 정보
    total_articles = Column(
        Integer,
        default=0,
        nullable=False,
        comment="총 기사 수"
    )
    total_recipients = Column(
        Integer,
        default=0,
        nullable=False,
        comment="총 수신자 수"
    )
    sent_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="발송 성공 수"
    )
    failed_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="발송 실패 수"
    )
    
    # 카테고리별 통계 (JSON)
    category_stats = Column(
        Text,  # JSON 형태: {"politics": 5, "economy": 3}
        nullable=True,
        comment="카테고리별 기사 수 (JSON)"
    )
    
    def __repr__(self) -> str:
        return f"<EmailDigest(date='{self.digest_date}', type='{self.digest_type}')>"