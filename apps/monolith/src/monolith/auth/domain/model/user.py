from datetime import datetime, timezone

from monolith.auth.domain.exceptions import user_exception as exceptions
from monolith.auth.domain.model.mixins import IdMixin, TimestampMixin, RevokedAtMixin


class User(IdMixin, TimestampMixin, RevokedAtMixin):
    """Класс модели-сущности пользователя"""

    def __init__(
            self,
            login: str,
            email: str,
            hashed_password: str,
            role_id: int,
            user_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            revoked_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, user_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        RevokedAtMixin.__init__(self, revoked_at)
        # Обязательные атрибуты
        self.id = user_id
        self.role_id = role_id
        self.login = login
        self.email = email
        self.hashed_password = hashed_password
        # Технические флаги
        self.is_verified = False
        # Валидация
        self._validate()

    def _validate(self):
        if not self.login:
            raise exceptions.InvalidUserLoginException("User login is required")
        if not self.email:
            raise exceptions.InvalidUserEmailException("User email is required")
        if not self.hashed_password:
            raise exceptions.InvalidUserPasswordException("User password is required")

    @property
    def is_active(self) -> bool:
        return self.revoked_at is None

    def deactivate(self):
        self.revoked_at = datetime.now(timezone.utc)
        self.touch()
