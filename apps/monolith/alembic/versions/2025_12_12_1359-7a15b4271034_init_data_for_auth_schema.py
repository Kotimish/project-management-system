"""init data for auth schema

Revision ID: 7a15b4271034
Revises: 3fb10c429b7c
Create Date: 2025-12-12 13:59:25.513248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a15b4271034'
down_revision: Union[str, Sequence[str], None] = '3fb10c429b7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade schema.
    Insert default roles into auth.roles.
    """
    op.execute(
        sa.text(
            """
                INSERT INTO auth.roles (name, slug, description, created_at, updated_at)
                VALUES
                    ('Admin', 'admin', 'Administrator role with full access', now(), now()),
                    ('User', 'user', 'Default user role with basic permissions', now(), now())
                ON CONFLICT (slug) DO NOTHING;
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM auth.roles WHERE slug IN ('admin', 'user');"
        )
    )
