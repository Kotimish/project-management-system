from datetime import datetime, timezone

from monolith.auth.domain.model.mixins import IdMixin, TimestampMixin, ExpirableMixin, RevokedAtMixin


class Session(IdMixin, TimestampMixin, ExpirableMixin, RevokedAtMixin):
    """Класс модели-сущности сессии пользователя"""

    def __init__(
            self,
            user_id: int,
            session_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            expires_at: datetime | None = None,
            revoked_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, session_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        ExpirableMixin.__init__(self, expires_at)
        RevokedAtMixin.__init__(self, revoked_at)
        # Обязательные атрибуты
        self.id = session_id
        self.user_id = user_id

    @property
    def is_active(self) -> bool:
        return (
            self.expires_at > datetime.now(timezone.utc) and
            self.revoked_at is None
        )