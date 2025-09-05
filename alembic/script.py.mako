"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """데이터베이스 업그레이드 (마이그레이션 적용)"""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """데이터베이스 다운그레이드 (마이그레이션 롤백)"""
    ${downgrades if downgrades else "pass"}