"""create projects table

Revision ID: badf501cc694
Revises: a61250d29c59
Create Date: 2025-12-14 20:54:16.156667

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'badf501cc694'
down_revision: Union[str, Sequence[str], None] = 'a61250d29c59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'projects',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            'owner_id',
            sa.Integer(), nullable=False
        ),
        sa.Column(
            'name',
            sa.String(length=100),
            nullable=False
        ),
        sa.Column(
            'description',
            sa.Text(), server_default='', nullable=True
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_projects')
        ),
        schema='project',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('projects', schema='project')
