from datetime import datetime

from monolith.project.domain.exceptions import project_exception as exceptions
from monolith.project.domain.model.mixins import IdMixin, TimestampMixin


class Project(IdMixin, TimestampMixin):
    """Доменная модель проекта"""

    def __init__(
            self,
            name: str,
            description: str,
            owner_id: int,
            project_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, project_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.name = name
        self.description = description
        self.owner_id = owner_id
        # Валидация
        self._validate()

    def _validate(self):
        if not self.name:
            raise exceptions.InvalidProjectNameException("Task status name is required")
        if not self.owner_id:
            raise exceptions.InvalidProjectOwnerIdException("Task status slug is required")
