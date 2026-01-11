from datetime import datetime

from monolith.project.domain.exceptions import task_status_exception as exceptions
from monolith.project.domain.model.mixins import IdMixin, TimestampMixin


class TaskStatus(IdMixin, TimestampMixin):
    """Доменная модель статусов задач"""
    def __init__(
            self,
            name: str,
            slug: str,
            description: str,
            status_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, status_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.name = name
        # Важно: slug должен быть уникальным
        self.slug = slug
        self.description = description
        # Валидация
        self._validate()

    def _validate(self):
        if not self.name:
            raise exceptions.InvalidTaskStatusNameException("Task status name is required")
        if not self.slug:
            raise exceptions.InvalidTaskStatusSlugException("Task status slug is required")