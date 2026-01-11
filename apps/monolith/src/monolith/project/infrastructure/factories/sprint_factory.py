from datetime import date

from monolith.project.application.interfaces.factories.sprint_factory import ISprintFactory
from monolith.project.domain.model import Sprint


class SprintFactory(ISprintFactory):
    """Интерфейс фабрики спринта проекта"""

    def create(self, name: str, project_id: int, start_date: date, end_date: date) -> Sprint:
        return Sprint(
            name=name,
            project_id=project_id,
            start_date=start_date,
            end_date=end_date,
        )
