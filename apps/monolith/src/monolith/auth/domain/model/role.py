from datetime import datetime

from monolith.auth.domain.exceptions import role_exception as exceptions
from monolith.auth.domain.model.mixins import IdMixin, TimestampMixin


class Role(IdMixin, TimestampMixin):
    """Класс модели-сущности роли пользователя"""
    def __init__(
            self,
            name: str,
            slug: str,
            description: str,
            role_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, role_id)
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
            raise exceptions.InvalidRoleNameException("Role name is required")
        if not self.slug:
            raise exceptions.InvalidRoleSlugException("Role slug is required")

    def update_description(self, description: str):
        self.description = description
        self.touch()
