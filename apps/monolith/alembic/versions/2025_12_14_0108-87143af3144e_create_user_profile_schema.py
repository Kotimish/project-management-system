"""create user profile schema

Revision ID: 87143af3144e
Revises: 7a15b4271034
Create Date: 2025-12-14 01:08:08.464874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87143af3144e'
down_revision: Union[str, Sequence[str], None] = '7a15b4271034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS user_profile")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA IF EXISTS user_profile")
