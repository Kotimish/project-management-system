"""create sessions table

Revision ID: 3fb10c429b7c
Revises: 30220490f5a3
Create Date: 2025-12-12 11:55:58.150224

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3fb10c429b7c'
down_revision: Union[str, Sequence[str], None] = '30220490f5a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'sessions',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'expires_at',
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            'revoked_at',
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['auth.users.id'],
            name=op.f('fk_sessions_user_id_users'),
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_sessions'),
        ),
        schema='auth',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sessions', schema='auth')
