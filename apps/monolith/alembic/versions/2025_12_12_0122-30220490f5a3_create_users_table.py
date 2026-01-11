"""create users table

Revision ID: 30220490f5a3
Revises: e1f833767dbc
Create Date: 2025-12-12 01:22:27.558894

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '30220490f5a3'
down_revision: Union[str, Sequence[str], None] = 'e1f833767dbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'login',
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            'email',
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            'hashed_password',
            sa.String(length=128),
            nullable=False,
        ),
        sa.Column(
            'role_id',
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
            'revoked_at',
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ['role_id'],
            ['auth.roles.id'],
            name=op.f('fk_users_role_id_roles'),
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_users'),
        ),
        sa.UniqueConstraint(
            'email',
            name=op.f('uq_users_email'),
        ),
        sa.UniqueConstraint(
            'login',
            name=op.f('uq_users_login'),
        ),
        schema='auth',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users', schema='auth')
