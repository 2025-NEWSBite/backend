"""
API 공통 스키마 정의
표준화된 API 응답 형식 및 에러 처리
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, Field
from datetime import datetime

DataType = TypeVar("DataType")


class APIResponse(BaseModel, Generic[DataType]):
    """
    표준 API 응답 형식
    모든 API 엔드포인트에서 일관된 응답 구조 제공
    """
    success: bool = Field(..., description="요청 성공 여부")
    message: str = Field(..., description="응답 메시지")
    data: Optional[DataType] = Field(None, description="응답 데이터")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="응답 시간")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "요청이 성공적으로 처리되었습니다",
                "data": {},
                "timestamp": "2024-01-01T12:00:00.000Z"
            }
        }


class PaginationMeta(BaseModel):
    """페이지네이션 메타데이터"""
    page: int = Field(..., description="현재 페이지 번호", ge=1)
    size: int = Field(..., description="페이지 크기", ge=1, le=100)
    total: int = Field(..., description="전체 항목 수", ge=0)
    pages: int = Field(..., description="전체 페이지 수", ge=0)
    has_next: bool = Field(..., description="다음 페이지 존재 여부")
    has_prev: bool = Field(..., description="이전 페이지 존재 여부")


class PaginatedResponse(BaseModel, Generic[DataType]):
    """
    페이지네이션 응답 형식
    목록 API에서 페이지네이션 정보와 함께 데이터 반환
    """
    items: List[DataType] = Field(..., description="데이터 목록")
    meta: PaginationMeta = Field(..., description="페이지네이션 메타데이터")


class ErrorDetail(BaseModel):
    """에러 상세 정보"""
    code: str = Field(..., description="에러 코드")
    message: str = Field(..., description="에러 메시지")
    field: Optional[str] = Field(None, description="에러 발생 필드")


class ErrorResponse(BaseModel):
    """
    에러 응답 형식
    API 에러 발생 시 표준화된 에러 정보 제공
    """
    success: bool = Field(False, description="요청 성공 여부")
    message: str = Field(..., description="에러 메시지")
    errors: Optional[List[ErrorDetail]] = Field(None, description="상세 에러 목록")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="에러 발생 시간")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "message": "요청 처리 중 오류가 발생했습니다",
                "errors": [
                    {
                        "code": "VALIDATION_ERROR",
                        "message": "이메일 형식이 올바르지 않습니다",
                        "field": "email"
                    }
                ],
                "timestamp": "2024-01-01T12:00:00.000Z"
            }
        }


class HealthCheckResponse(BaseModel):
    """헬스체크 응답"""
    status: str = Field(..., description="서비스 상태")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="확인 시간")
    version: str = Field(..., description="API 버전")
    database: str = Field(..., description="데이터베이스 연결 상태")
    redis: str = Field(..., description="Redis 연결 상태")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T12:00:00.000Z",
                "version": "1.0.0",
                "database": "connected",
                "redis": "connected"
            }
        }


# 공통 응답 생성 함수들

def create_success_response(
    data: Any = None,
    message: str = "요청이 성공적으로 처리되었습니다"
) -> Dict[str, Any]:
    """성공 응답 생성"""
    return APIResponse[Any](
        success=True,
        message=message,
        data=data
    ).dict()


def create_error_response(
    message: str,
    errors: Optional[List[ErrorDetail]] = None,
    status_code: int = 400
) -> Dict[str, Any]:
    """에러 응답 생성"""
    return ErrorResponse(
        message=message,
        errors=errors
    ).dict()


def create_paginated_response(
    items: List[Any],
    page: int,
    size: int,
    total: int
) -> Dict[str, Any]:
    """페이지네이션 응답 생성"""
    pages = (total + size - 1) // size  # 전체 페이지 수 계산
    
    paginated_data = PaginatedResponse[Any](
        items=items,
        meta=PaginationMeta(
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )
    )
    
    return create_success_response(
        data=paginated_data.dict(),
        message=f"총 {total}개의 항목을 조회했습니다"
    )