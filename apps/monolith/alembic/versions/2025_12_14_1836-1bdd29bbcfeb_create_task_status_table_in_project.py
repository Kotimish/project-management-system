"""create task status table in project

Revision ID: 1bdd29bbcfeb
Revises: b0fe1f867fdd
Create Date: 2025-12-14 18:36:18.789114

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1bdd29bbcfeb'
down_revision: Union[str, Sequence[str], None] = 'b0fe1f867fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'task_status',
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
            name=op.f('pk_task_status'),
        ),
        sa.UniqueConstraint(
            'name',
            name=op.f('uq_task_status_name'),
        ),
        sa.UniqueConstraint(
            'slug',
            name=op.f('uq_task_status_slug'),
        ),
        schema='project',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('task_status', schema='project')
