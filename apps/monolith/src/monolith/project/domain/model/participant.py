from datetime import datetime

from monolith.project.domain.exceptions import participant_exception as exceptions
from monolith.project.domain.model.mixins import IdMixin, TimestampMixin


class Participant(IdMixin, TimestampMixin):
    """Доменная сущность участники"""

    def __init__(
            self,
            auth_user_id: int,
            project_id: int,
            participant_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, participant_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.auth_user_id = auth_user_id
        self.project_id = project_id
        # Валидация
        self._validate()

    def _validate(self):
        if not self.auth_user_id:
            raise exceptions.InvalidProjectAuthUserIdException("Auth user id is required")
        if not self.project_id:
            raise exceptions.InvalidProjectProjectIdException("Project id is required")
