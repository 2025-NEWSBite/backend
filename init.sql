-- 뉴스한입(NewsBite) 데이터베이스 초기화 스크립트
-- PostgreSQL용 초기 데이터 및 확장 설정

-- 필요한 확장 설치
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- UUID 생성 함수
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- 유사성 검색
CREATE EXTENSION IF NOT EXISTS "unaccent";   -- 악센트 제거

-- 데이터베이스 인코딩 확인 (UTF-8이어야 함)
SHOW server_encoding;

-- 기본 데이터 삽입

-- 1. 이메일 템플릿 초기 데이터
INSERT INTO email_templates (id, name, email_type, subject_template, html_template, language, created_at, updated_at) VALUES
(uuid_generate_v4(), 'daily_digest_ko', 'daily_digest', '[뉴스한입] 오늘의 뉴스 ({date})', '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>오늘의 뉴스</title></head><body><h1>안녕하세요, {user_name}님!</h1><p>오늘의 선별된 뉴스를 전해드립니다.</p>{news_content}</body></html>', 'ko', NOW(), NOW()),

(uuid_generate_v4(), 'weekly_digest_ko', 'weekly_digest', '[뉴스한입] 이번 주 뉴스 요약 ({week})', '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>주간 뉴스</title></head><body><h1>안녕하세요, {user_name}님!</h1><p>이번 주의 주요 뉴스를 정리해드립니다.</p>{news_content}</body></html>', 'ko', NOW(), NOW()),

(uuid_generate_v4(), 'welcome_ko', 'welcome', '[뉴스한입] 가입을 환영합니다!', '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>환영합니다</title></head><body><h1>뉴스한입에 가입해주셔서 감사합니다!</h1><p>개인맞춤 뉴스 서비스로 더욱 편리하게 뉴스를 받아보세요.</p></body></html>', 'ko', NOW(), NOW()),

(uuid_generate_v4(), 'verification_ko', 'verification', '[뉴스한입] 이메일 인증을 완료해주세요', '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>이메일 인증</title></head><body><h1>이메일 인증</h1><p>아래 버튼을 클릭하여 이메일 인증을 완료해주세요.</p><a href="{verification_url}">인증하기</a></body></html>', 'ko', NOW(), NOW());

-- 2. 뉴스 카테고리별 샘플 키워드
INSERT INTO news_keywords (id, keyword, frequency, is_trending, trend_score, created_at, updated_at, last_seen) VALUES
(uuid_generate_v4(), '대통령', 100, true, 0.9, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '경제', 85, true, 0.8, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '코로나', 120, true, 0.95, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '부동산', 75, true, 0.7, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '주식', 60, false, 0.6, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '정치', 90, true, 0.85, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '사회', 70, false, 0.65, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '문화', 45, false, 0.4, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '스포츠', 55, false, 0.5, NOW(), NOW(), NOW()),
(uuid_generate_v4(), '연예', 40, false, 0.3, NOW(), NOW(), NOW());

-- 3. 인덱스 생성 (성능 최적화)
-- 사용자 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- 뉴스 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_news_articles_url ON news_articles(url);
CREATE INDEX IF NOT EXISTS idx_news_articles_category ON news_articles(category);
CREATE INDEX IF NOT EXISTS idx_news_articles_published_at ON news_articles(published_at);
CREATE INDEX IF NOT EXISTS idx_news_articles_status ON news_articles(status);
CREATE INDEX IF NOT EXISTS idx_news_articles_importance_score ON news_articles(importance_score);

-- 검색 최적화를 위한 복합 인덱스
CREATE INDEX IF NOT EXISTS idx_news_articles_category_published ON news_articles(category, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_articles_status_published ON news_articles(status, published_at DESC);

-- 키워드 관련 인덱스
CREATE INDEX IF NOT EXISTS idx_news_keywords_keyword ON news_keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_news_keywords_trending ON news_keywords(is_trending, trend_score DESC);

-- 이메일 로그 인덱스
CREATE INDEX IF NOT EXISTS idx_email_logs_recipient ON email_logs(recipient_email);
CREATE INDEX IF NOT EXISTS idx_email_logs_status ON email_logs(status);
CREATE INDEX IF NOT EXISTS idx_email_logs_type_sent ON email_logs(email_type, sent_at DESC);

-- 이메일 다이제스트 인덱스
CREATE INDEX IF NOT EXISTS idx_email_digests_date_type ON email_digests(digest_date DESC, digest_type);

-- 4. 전문 검색을 위한 텍스트 검색 설정
-- 뉴스 제목과 내용에 대한 전문 검색 인덱스
CREATE INDEX IF NOT EXISTS idx_news_articles_title_search 
ON news_articles USING gin(to_tsvector('korean', title));

CREATE INDEX IF NOT EXISTS idx_news_articles_content_search 
ON news_articles USING gin(to_tsvector('korean', content));

-- 5. 트리거 함수 생성 (업데이트 시간 자동 갱신)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 6. 데이터베이스 통계 정보 업데이트
ANALYZE;

-- 초기화 완료 메시지
SELECT '뉴스한입 데이터베이스 초기화가 완료되었습니다.' as message;