"""create roles table

Revision ID: e1f833767dbc
Revises: 02f9545c9d6b
Create Date: 2025-12-12 00:40:19.957669

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e1f833767dbc'
down_revision: Union[str, Sequence[str], None] = '02f9545c9d6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'roles',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'name',
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            'slug',
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            'description',
            sa.Text(),
            server_default='',
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
            name=op.f('pk_roles'),
        ),
        sa.UniqueConstraint(
            'name',
            name=op.f('uq_roles_name'),
        ),
        sa.UniqueConstraint(
            'slug',
            name=op.f('uq_roles_slug'),
        ),
        schema='auth',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('roles', schema='auth')
