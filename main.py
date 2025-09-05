"""
뉴스한입(NewsBite) 백엔드 메인 애플리케이션
개인맞춤 뉴스 요약 이메일 서비스 API
"""

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.core.config import settings
from app.core.schemas import create_success_response, HealthCheckResponse
from app.core.exceptions import (
    BaseCustomException,
    custom_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.db.database import init_db, close_db

# 로그 설정
logger.remove()
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    colorize=True
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 라이프사이클 관리
    시작 시 데이터베이스 초기화, 종료 시 정리 작업
    """
    try:
        # 애플리케이션 시작
        logger.info("🚀 뉴스한입 백엔드 서버 시작 중...")
        
        # 데이터베이스 연결 및 초기화
        await init_db()
        logger.success("✅ 데이터베이스 연결 성공")
        
        logger.success("🎉 뉴스한입 백엔드 서버 시작 완료!")
        yield
        
    except Exception as e:
        logger.error(f"❌ 서버 시작 중 오류 발생: {e}")
        raise
    finally:
        # 애플리케이션 종료
        logger.info("🛑 뉴스한입 백엔드 서버 종료 중...")
        
        # 데이터베이스 연결 정리
        await close_db()
        logger.info("🔌 데이터베이스 연결 종료")
        
        logger.info("👋 뉴스한입 백엔드 서버 종료 완료")


# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # 프로덕션에서는 문서 비활성화
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# 예외 핸들러 등록
app.add_exception_handler(BaseCustomException, custom_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Page-Count"]
)

# 향후 API 라우터들을 등록할 예정
# app.include_router(auth_router, prefix="/api/v1/auth", tags=["인증"])
# app.include_router(news_router, prefix="/api/v1/news", tags=["뉴스"])
# app.include_router(users_router, prefix="/api/v1/users", tags=["사용자"])


@app.get("/", response_model=dict, tags=["루트"])
async def root():
    """
    루트 엔드포인트
    서버 기본 정보 반환
    """
    return create_success_response(
        data={
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "description": settings.DESCRIPTION,
            "docs": "/docs" if settings.DEBUG else None,
            "timestamp": datetime.utcnow()
        },
        message="뉴스한입 API 서버가 정상 작동 중입니다"
    )


@app.get("/health", response_model=dict, tags=["헬스체크"])
async def health_check():
    """
    상세 헬스체크 엔드포인트
    서버 및 연결된 서비스들의 상태 확인
    """
    try:
        # TODO: 실제 데이터베이스 및 Redis 연결 상태 확인
        # 현재는 기본값으로 설정
        database_status = "connected"
        redis_status = "connected"
        
        health_data = HealthCheckResponse(
            status="healthy",
            version=settings.VERSION,
            database=database_status,
            redis=redis_status
        )
        
        return create_success_response(
            data=health_data.dict(),
            message="모든 서비스가 정상 작동 중입니다"
        )
        
    except Exception as e:
        logger.error(f"헬스체크 중 오류 발생: {e}")
        health_data = HealthCheckResponse(
            status="unhealthy",
            version=settings.VERSION,
            database="error",
            redis="error"
        )
        
        return {
            "success": False,
            "message": "일부 서비스에 문제가 있습니다",
            "data": health_data.dict(),
            "timestamp": datetime.utcnow()
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )