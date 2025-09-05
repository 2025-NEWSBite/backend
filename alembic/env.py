"""
Alembic 환경 설정 파일
데이터베이스 마이그레이션을 위한 설정
"""

import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 앱의 모델들을 import
from app.db.base import Base
from app.db.models import *  # 모든 모델 import

# Alembic Config 객체
config = context.config

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 메타데이터 설정
target_metadata = Base.metadata

# 환경 변수에서 데이터베이스 URL 가져오기
def get_database_url():
    """환경 변수 또는 기본값에서 데이터베이스 URL 가져오기"""
    from dotenv import load_dotenv
    load_dotenv()
    
    return os.getenv(
        "DATABASE_URL",
        "postgresql://newsbite_user:newsbite_password@localhost:5432/newsbite"
    )

def run_migrations_offline() -> None:
    """
    오프라인 모드에서 마이그레이션 실행
    데이터베이스 연결 없이 SQL 스크립트 생성
    """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """실제 마이그레이션 실행"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    비동기 모드에서 마이그레이션 실행
    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_database_url()
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    온라인 모드에서 마이그레이션 실행
    실제 데이터베이스 연결을 통해 실행
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()