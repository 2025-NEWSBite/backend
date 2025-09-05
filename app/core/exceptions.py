"""
커스텀 예외 클래스 및 에러 핸들러
애플리케이션 전체에서 사용할 예외 클래스들 정의
"""

from typing import Any, Dict, Optional, List
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from loguru import logger


class BaseCustomException(Exception):
    """커스텀 예외 베이스 클래스"""
    
    def __init__(
        self,
        message: str = "오류가 발생했습니다",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BaseCustomException):
    """유효성 검증 실패"""
    
    def __init__(
        self,
        message: str = "입력 데이터가 유효하지 않습니다",
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details or {}
        )
        if field:
            self.details["field"] = field


class AuthenticationError(BaseCustomException):
    """인증 실패"""
    
    def __init__(
        self,
        message: str = "인증이 필요합니다",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details or {}
        )


class AuthorizationError(BaseCustomException):
    """권한 부족"""
    
    def __init__(
        self,
        message: str = "접근 권한이 없습니다",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=details or {}
        )


class NotFoundError(BaseCustomException):
    """리소스를 찾을 수 없음"""
    
    def __init__(
        self,
        message: str = "요청한 리소스를 찾을 수 없습니다",
        resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND_ERROR",
            details=details or {}
        )
        if resource:
            self.details["resource"] = resource


class ConflictError(BaseCustomException):
    """데이터 충돌"""
    
    def __init__(
        self,
        message: str = "데이터 충돌이 발생했습니다",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT_ERROR",
            details=details or {}
        )


class RateLimitError(BaseCustomException):
    """요청 제한 초과"""
    
    def __init__(
        self,
        message: str = "요청 한도를 초과했습니다",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_ERROR",
            details=details or {}
        )
        if retry_after:
            self.details["retry_after"] = retry_after


class DatabaseError(BaseCustomException):
    """데이터베이스 관련 오류"""
    
    def __init__(
        self,
        message: str = "데이터베이스 오류가 발생했습니다",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
            details=details or {}
        )


class ExternalServiceError(BaseCustomException):
    """외부 서비스 연동 오류"""
    
    def __init__(
        self,
        message: str = "외부 서비스 연동 중 오류가 발생했습니다",
        service: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details or {}
        )
        if service:
            self.details["service"] = service


# 에러 핸들러 함수들

async def custom_exception_handler(request: Request, exc: BaseCustomException) -> JSONResponse:
    """커스텀 예외 핸들러"""
    
    # 로그 기록
    logger.error(
        f"Custom exception occurred: {exc.error_code} - {exc.message} | "
        f"Path: {request.url.path} | Method: {request.method} | "
        f"Details: {exc.details}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "errors": [
                {
                    "code": exc.error_code,
                    "message": exc.message,
                    **exc.details
                }
            ],
            "timestamp": str(exc.details.get("timestamp") or "")
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP 예외 핸들러"""
    
    # 로그 기록
    logger.warning(
        f"HTTP exception occurred: {exc.status_code} - {exc.detail} | "
        f"Path: {request.url.path} | Method: {request.method}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "errors": [
                {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail
                }
            ],
            "timestamp": ""
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """일반 예외 핸들러"""
    
    # 로그 기록
    logger.error(
        f"Unexpected exception occurred: {type(exc).__name__} - {str(exc)} | "
        f"Path: {request.url.path} | Method: {request.method}",
        exc_info=exc
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "서버 내부 오류가 발생했습니다",
            "errors": [
                {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "예기치 않은 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                }
            ],
            "timestamp": ""
        }
    )