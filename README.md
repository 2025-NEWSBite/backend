# NewsBite Backend (뉴스한입 백엔드)

개인맞춤 뉴스 요약 이메일 서비스 백엔드 API

## 프로젝트 개요

NewsBite는 사용자의 관심사에 맞춘 뉴스를 AI로 요약하여 이메일로 전송하는 개인화된 뉴스 서비스입니다.

### 주요 기능

- 🤖 **AI 뉴스 요약**: Transformer 모델을 활용한 한국어 뉴스 요약
- 📧 **개인화 이메일**: 사용자 선호도에 따른 맞춤형 뉴스 다이제스트
- 🔍 **뉴스 크롤링**: 실시간 뉴스 수집 및 분류
- 👤 **사용자 관리**: Firebase 인증 및 개인 설정 관리
- 📊 **감정 분석**: 뉴스 기사의 감정 톤 분석

## 기술 스택

- **웹 프레임워크**: FastAPI 0.104.1
- **데이터베이스**: PostgreSQL (AsyncPG)
- **ORM**: SQLAlchemy 2.0 (Async)
- **마이그레이션**: Alembic
- **캐싱**: Redis
- **AI/ML**: 
  - Transformers (Hugging Face)
  - PyTorch
  - Sentence Transformers
- **백그라운드 작업**: Celery
- **이메일**: FastAPI-Mail
- **인증**: Firebase Auth, JWT
- **배포**: Docker

## 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.development` 파일을 참고하여 환경 변수를 설정하세요.

주요 설정값:
- `DATABASE_URL`: PostgreSQL 연결 정보
- `REDIS_URL`: Redis 연결 정보
- `SECRET_KEY`: JWT 토큰 암호화 키
- `OPENAI_API_KEY`: OpenAI API 키 (선택사항)

### 3. 데이터베이스 설정

```bash
# 데이터베이스 마이그레이션
alembic upgrade head
```

### 4. 서버 실행

```bash
# 개발 서버 실행
python main.py

# 또는 uvicorn으로 직접 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

서버가 실행되면 다음 URL에서 접근 가능합니다:
- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/health

## 개발 가이드

### 데이터베이스 마이그레이션

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 코드 품질

```bash
# 코드 포매팅
black .
isort .

# 린팅
flake8

# 테스트 실행
pytest
pytest -v  # 상세 출력
```

### Docker로 실행

```bash
# 이미지 빌드
docker build -t newsbite-backend .

# 컨테이너 실행
docker run -p 8000:8000 newsbite-backend
```

## API 구조

```
/api/v1/
├── /auth         # 사용자 인증 (예정)
├── /users        # 사용자 관리 (예정)
├── /news         # 뉴스 관련 (예정)
└── /email        # 이메일 관련 (예정)
```

### 현재 사용 가능한 엔드포인트

- `GET /`: 서버 정보
- `GET /health`: 헬스체크

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/v1/          # API 라우터
│   ├── core/            # 핵심 유틸리티 (설정, 보안, 예외처리)
│   ├── db/              # 데이터베이스 모델 및 연결
│   │   └── models/      # SQLAlchemy 모델
│   ├── services/        # 비즈니스 로직
│   ├── ai/              # AI/ML 관련 기능
│   ├── crawler/         # 뉴스 크롤링
│   └── email/           # 이메일 서비스
├── alembic/             # 데이터베이스 마이그레이션
├── main.py              # FastAPI 애플리케이션 엔트리포인트
├── requirements.txt     # Python 의존성
└── Dockerfile          # Docker 설정
```

## 라이선스

MIT License
