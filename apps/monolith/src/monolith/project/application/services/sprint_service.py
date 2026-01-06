from datetime import date

from monolith.project.application.dto.sprint import UpdateSprintCommand
from monolith.project.application.interfaces.factories.sprint_factory import ISprintFactory
from monolith.project.application.interfaces.services.sprint_service import ISprintService
from monolith.project.domain.exceptions.sprint_exception import SprintUnauthorizedError
from monolith.project.domain.interfaces.repositories.sprint_repository import ISprintRepository
from monolith.project.domain.model import Sprint


class SprintService(ISprintService):
    """Интерфейс сервиса Спринта"""
    def __init__(
            self,
            factory: ISprintFactory,
            repository: ISprintRepository
    ):
        self.factory = factory
        self.repository = repository

    async def create_sprint(self, name: str, project_id: int, start_date: date, end_date: date) -> Sprint:
        sprint = self.factory.create(name, project_id, start_date, end_date)
        sprint = await self.repository.add(sprint)
        return sprint

    async def get_sprint_by_id(self, sprint_id: int) -> Sprint:
        return await self.repository.get_by_id(sprint_id)

    async def get_all_sprint_by_project_id(self, project_id: int) -> list[Sprint]:
        return await self.repository.get_all_by_project_id(project_id)

    async def update_sprint(self, project_id: int, sprint_id: int, data: UpdateSprintCommand) -> Sprint:
        sprint = await self.repository.get_by_id(sprint_id)
        if sprint.project_id != project_id:
            raise SprintUnauthorizedError("Sprint does not belong to project")
        if data.name is not None:
            sprint.name = data.name
        if data.start_date is not None:
            sprint.start_date = data.start_date
        if data.end_date is not None:
            sprint.end_date = data.end_date
        sprint.touch()
        sprint = await self.repository.update(sprint_id, sprint)
        return sprint
