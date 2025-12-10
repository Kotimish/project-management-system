from datetime import datetime

from monolith.auth.domain.model.mixins import IdMixin, TimestampMixin


class User(IdMixin, TimestampMixin):
    """Класс модели-сущности пользователя"""

    def __init__(
            self,
            login: str,
            email: str,
            hashed_password: str,
            role_id: int,
            user_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, user_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.id = user_id
        self.role_id = role_id
        self.login = login
        self.email = email
        self.hashed_password = hashed_password
        # Технические флаги
        self.is_active = True
        self.is_verified = False
        # Валидация
        self._validate()

    def _validate(self):
        # TODO прописать валидацию обязательных атрибутов
        pass

    def deactivate(self):
        self.is_active = False
        self.touch()
