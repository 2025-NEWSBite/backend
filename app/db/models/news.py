"""
뉴스 관련 데이터베이스 모델
"""

from sqlalchemy import Boolean, Column, String, Text, Integer, DateTime, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum
from datetime import datetime
from app.db.base import Base, TimestampMixin, UUIDMixin


class NewsCategory(str, Enum):
    """뉴스 카테고리 enum"""
    POLITICS = "politics"        # 정치
    ECONOMY = "economy"          # 경제
    SOCIETY = "society"          # 사회
    CULTURE = "culture"          # 문화
    INTERNATIONAL = "international"  # 국제
    SPORTS = "sports"            # 스포츠
    ENTERTAINMENT = "entertainment"  # 연예
    IT = "it"                    # IT/과학
    HEALTH = "health"            # 건강/의료
    EDUCATION = "education"      # 교육


class NewsStatus(str, Enum):
    """뉴스 처리 상태 enum"""
    CRAWLED = "crawled"          # 크롤링 완료
    PROCESSING = "processing"    # 처리 중
    SUMMARIZED = "summarized"    # 요약 완료
    FAILED = "failed"            # 처리 실패
    PUBLISHED = "published"      # 발행 완료


class SentimentType(str, Enum):
    """감정 분석 결과 enum"""
    POSITIVE = "positive"        # 긍정적
    NEGATIVE = "negative"        # 부정적
    NEUTRAL = "neutral"          # 중립적


class NewsArticle(Base, UUIDMixin, TimestampMixin):
    """
    뉴스 기사 모델
    크롤링된 원본 뉴스 기사 정보 저장
    """
    __tablename__ = "news_articles"

    # 기본 정보
    title = Column(
        String(500),
        nullable=False,
        comment="뉴스 제목"
    )
    content = Column(
        Text,
        nullable=False,
        comment="뉴스 본문"
    )
    summary = Column(
        Text,
        nullable=True,
        comment="AI 생성 요약"
    )
    
    # 메타데이터
    url = Column(
        String(1000),
        unique=True,
        nullable=False,
        index=True,
        comment="원본 뉴스 URL"
    )
    source = Column(
        String(100),
        nullable=False,
        comment="뉴스 출처 (예: 연합뉴스, 조선일보)"
    )
    author = Column(
        String(100),
        nullable=True,
        comment="기자명"
    )
    
    # 카테고리 및 분류
    category = Column(
        SQLEnum(NewsCategory),
        nullable=False,
        index=True,
        comment="뉴스 카테고리"
    )
    tags = Column(
        ARRAY(String),
        nullable=True,
        comment="뉴스 태그 배열"
    )
    
    # 발행 정보
    published_at = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="뉴스 발행 시간"
    )
    crawled_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="크롤링 시간"
    )
    
    # 처리 상태
    status = Column(
        SQLEnum(NewsStatus),
        default=NewsStatus.CRAWLED,
        nullable=False,
        comment="처리 상태"
    )
    
    # AI 분석 결과
    sentiment = Column(
        SQLEnum(SentimentType),
        nullable=True,
        comment="감정 분석 결과"
    )
    sentiment_score = Column(
        Float,
        nullable=True,
        comment="감정 점수 (-1.0 ~ 1.0)"
    )
    importance_score = Column(
        Float,
        default=0.0,
        nullable=False,
        comment="중요도 점수 (0.0 ~ 1.0)"
    )
    
    # 통계 정보
    view_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="조회수"
    )
    share_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="공유수"
    )
    
    # 이미지 정보
    thumbnail_url = Column(
        String(1000),
        nullable=True,
        comment="썸네일 이미지 URL"
    )
    
    # 관계 설정
    summaries = relationship(
        "NewsSummary",
        back_populates="article",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<NewsArticle(title='{self.title[:50]}...', source='{self.source}')>"


class NewsSummary(Base, UUIDMixin, TimestampMixin):
    """
    뉴스 요약 모델
    여러 기사를 그룹화하여 생성된 요약 정보
    """
    __tablename__ = "news_summaries"

    # 외래키
    article_id = Column(
        "article_id",
        UUIDMixin.id.type,
        # ForeignKey("news_articles.id"),
        nullable=False,
        comment="원본 기사 ID"
    )
    
    # 요약 정보
    title = Column(
        String(300),
        nullable=False,
        comment="요약 제목"
    )
    content = Column(
        Text,
        nullable=False,
        comment="요약 내용"
    )
    key_points = Column(
        ARRAY(String),
        nullable=True,
        comment="핵심 포인트 배열"
    )
    
    # 요약 타입
    summary_type = Column(
        SQLEnum("short", "medium", "long", name="summary_type_enum"),
        default="medium",
        nullable=False,
        comment="요약 길이 타입"
    )
    
    # AI 모델 정보
    model_name = Column(
        String(100),
        nullable=True,
        comment="사용된 AI 모델명"
    )
    model_version = Column(
        String(50),
        nullable=True,
        comment="AI 모델 버전"
    )
    confidence_score = Column(
        Float,
        nullable=True,
        comment="요약 신뢰도 점수 (0.0 ~ 1.0)"
    )
    
    # 언어
    language = Column(
        String(10),
        default="ko",
        nullable=False,
        comment="요약 언어"
    )
    
    # 관계 설정
    article = relationship("NewsArticle", back_populates="summaries")
    
    def __repr__(self) -> str:
        return f"<NewsSummary(title='{self.title}', type='{self.summary_type}')>"


class NewsKeyword(Base, UUIDMixin, TimestampMixin):
    """
    뉴스 키워드 모델
    트렌딩 키워드 및 검색어 관리
    """
    __tablename__ = "news_keywords"

    # 키워드 정보
    keyword = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="키워드"
    )
    frequency = Column(
        Integer,
        default=1,
        nullable=False,
        comment="등장 빈도"
    )
    
    # 카테고리별 빈도
    category_frequency = Column(
        Text,  # JSON 형태로 저장: {"politics": 10, "economy": 5}
        nullable=True,
        comment="카테고리별 등장 빈도 (JSON)"
    )
    
    # 트렌드 정보
    is_trending = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="트렌딩 키워드 여부"
    )
    trend_score = Column(
        Float,
        default=0.0,
        nullable=False,
        comment="트렌드 점수"
    )
    
    # 시간별 통계
    last_seen = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="마지막 등장 시간"
    )
    
    def __repr__(self) -> str:
        return f"<NewsKeyword(keyword='{self.keyword}', frequency={self.frequency})>"