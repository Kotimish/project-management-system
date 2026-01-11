"""init data for task status

Revision ID: a61250d29c59
Revises: 1bdd29bbcfeb
Create Date: 2025-12-14 19:53:42.103509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Text



# revision identifiers, used by Alembic.
revision: str = 'a61250d29c59'
down_revision: Union[str, Sequence[str], None] = '1bdd29bbcfeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    task_status_table = table(
        'task_status',
        column('name', String(100)),
        column('slug', String(100)),
        column('description', Text),
        schema='project',
    )

    op.bulk_insert(task_status_table, [
        {
            'name': 'В ожидании',
            'slug': 'pending',
            'description': 'Задача находится в очереди на выполнение'
        },
        {
            'name': 'В работе',
            'slug': 'in_progress',
            'description': 'Задача находится в процессе выполнения'
        },
        {
            'name': 'На проверке',
            'slug': 'review',
            'description': 'Задача находится на проверке'
        },
        {
            'name': 'Выполнено',
            'slug': 'done',
            'description': 'Задача выполнена'
        }
    ])

def downgrade() -> None:
    """Downgrade schema."""
    task_status_table = table(
        'task_status',
        column('slug', String(100)),
        schema='project',
    )
    # Удаление по уникальной метке
    op.execute(
        task_status_table.
        delete()
        .where(
            task_status_table.columns.slug.in_(
                [
                    'pending',
                    'in_progress',
                    'review',
                    'done'
                ]
            )
        ),
    )
