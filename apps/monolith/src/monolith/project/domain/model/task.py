from datetime import datetime

from monolith.project.domain.exceptions import task_exception as exceptions
from monolith.project.domain.model.mixins import IdMixin, TimestampMixin


class Task(IdMixin, TimestampMixin):
    """Доменная модель Задачи"""

    def __init__(
            self,
            title: str,
            description: str,
            project_id: int,
            status_id: int,
            assignee_id: int | None,
            sprint_id: int | None = None,
            task_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, task_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.title = title
        self.description = description
        self.project_id = project_id
        self.status_id = status_id
        self.assignee_id = assignee_id
        self.sprint_id = sprint_id
        # Валидация
        self._validate()

    def _validate(self):
        if not self.title:
            raise exceptions.InvalidTaskTitleException("Project name is required")
        if not self.project_id:
            raise exceptions.InvalidProjectIdException("Project name is required")
        if not self.status_id:
            raise exceptions.InvalidStatusIdException("Project name is required")
