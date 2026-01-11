"""create project participants table

Revision ID: c56928592a0d
Revises: badf501cc694
Create Date: 2025-12-14 22:05:56.555188

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c56928592a0d'
down_revision: Union[str, Sequence[str], None] = 'badf501cc694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'participants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('auth_user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['project.projects.id'],
                                name=op.f('fk_participants_project_id_projects')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_participants')),
        schema='project'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('participants', schema='project')
