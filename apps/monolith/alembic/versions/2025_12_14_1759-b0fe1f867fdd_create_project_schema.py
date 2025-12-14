"""create project schema

Revision ID: b0fe1f867fdd
Revises: 6c9bf61d4304
Create Date: 2025-12-14 17:59:38.734072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0fe1f867fdd'
down_revision: Union[str, Sequence[str], None] = '6c9bf61d4304'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS project")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA IF EXISTS project")
