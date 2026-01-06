from datetime import datetime

from monolith.project.domain.model import Task, TaskStatus


class TaskWithStatus(Task):
    """Доменная модель Задачи с агрегированными значениями"""

    def __init__(
            self,
            title: str,
            description: str,
            project_id: int,
            status_id: int,
            status: TaskStatus,
            assignee_id: int | None,
            sprint_id: int | None = None,
            task_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов
        super().__init__(
            title=title,
            description=description,
            project_id=project_id,
            status_id=status_id,
            assignee_id=assignee_id,
            sprint_id=sprint_id,
            task_id=task_id,
            created_at=created_at,
            updated_at=updated_at
        )
        # Обязательные атрибуты
        self.status = status
