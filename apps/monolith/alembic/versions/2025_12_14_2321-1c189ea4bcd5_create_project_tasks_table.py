"""create project tasks table

Revision ID: 1c189ea4bcd5
Revises: 55fea1ab5b36
Create Date: 2025-12-14 23:21:10.958827

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1c189ea4bcd5'
down_revision: Union[str, Sequence[str], None] = '55fea1ab5b36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'tasks',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            'title',
            sa.String(length=255),
            nullable=False
        ),
        sa.Column(
            'description',
            sa.Text(),
            server_default='',
            nullable=True,
        ),
        sa.Column(
            'assignee_id',
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            'project_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'status_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'sprint_id',
            sa.Integer(),
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
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['project.projects.id'],
            name=op.f('fk_tasks_project_id_projects'
                      ),
        ),
        sa.ForeignKeyConstraint(
            ['sprint_id'],
            ['project.sprints.id'],
            name=op.f('fk_tasks_sprint_id_sprints'
                      ),
        ),
        sa.ForeignKeyConstraint(
            ['status_id'],
            ['project.task_status.id'],
            name=op.f('fk_tasks_status_id_task_status'),
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_tasks'),
        ),
        schema='project',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tasks', schema='project')
