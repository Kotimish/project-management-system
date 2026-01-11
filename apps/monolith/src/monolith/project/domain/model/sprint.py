from datetime import datetime, date

from monolith.project.domain.exceptions import sprint_exception as exceptions
from monolith.project.domain.model.mixins import IdMixin, TimestampMixin


class Sprint(IdMixin, TimestampMixin):
    """Доменная модель Спринта - ограниченного по времени периода"""
    def __init__(
            self,
            name: str,
            project_id: int,
            start_date: date,
            end_date: date,
            sprint_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, sprint_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.name = name
        self.project_id = project_id
        self.start_date = start_date
        self.end_date = end_date
        # Валидация
        self._validate()

    def _validate(self):
        if not self.name:
            raise exceptions.InvalidSprintNameException("Sprint name is required")
        if not self.project_id:
            raise exceptions.InvalidProjectIdException("Spint project id is required")
        if not self.start_date or not self.end_date:
            raise exceptions.InvalidSpingDateException("Spring date is required")
        if self.start_date > self.end_date:
            raise exceptions.InvalidSpingDateException("Start date cannot be later than end date")
