"""
기본 모델 클래스들
모든 데이터베이스 모델이 상속받을 베이스 클래스 정의
"""

from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import uuid


@as_declarative()
class Base:
    """
    모든 모델의 베이스 클래스
    공통 필드와 메서드 정의
    """
    id: Any
    __name__: str
    
    # 자동으로 테이블명 생성 (클래스명을 snake_case로 변환)
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampMixin:
    """
    생성/수정 시간 자동 관리 믹스인
    모든 모델에서 공통으로 사용
    """
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="생성 시간"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="수정 시간"
    )


class UUIDMixin:
    """
    UUID 기본키 믹스인
    보안과 확장성을 위해 UUID 사용
    """
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="고유 식별자"
    )