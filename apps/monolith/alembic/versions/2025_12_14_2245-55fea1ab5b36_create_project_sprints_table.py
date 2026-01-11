"""create project sprints table

Revision ID: 55fea1ab5b36
Revises: c56928592a0d
Create Date: 2025-12-14 22:45:07.916075

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '55fea1ab5b36'
down_revision: Union[str, Sequence[str], None] = 'c56928592a0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'sprints',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'project_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'name',
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            'start_date',
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            'end_date',
            sa.Date(), nullable=False,
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
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['project.projects.id'],
            name=op.f('fk_sprints_project_id_projects'),
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_sprints'),
        ),
        sa.UniqueConstraint(
            'name',
            name=op.f('uq_sprints_name'),
        ),
        schema='project',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sprints', schema='project')
