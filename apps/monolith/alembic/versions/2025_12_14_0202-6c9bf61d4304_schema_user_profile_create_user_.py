"""schema user_profile: create user profiles table

Revision ID: 6c9bf61d4304
Revises: 87143af3144e
Create Date: 2025-12-14 02:02:49.818946

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6c9bf61d4304'
down_revision: Union[str, Sequence[str], None] = '87143af3144e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user_profiles',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'auth_user_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'display_name',
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            'first_name',
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            'middle_name',
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            'last_name',
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            'description',
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            'birthdate',
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            'phone',
            sa.String(length=20),
            nullable=True,
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
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_user_profiles'),
        ),
        sa.UniqueConstraint(
            'auth_user_id',
            name=op.f('uq_user_profiles_auth_user_id'),
        ),
        schema='user_profile',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_profiles', schema='user_profile')
