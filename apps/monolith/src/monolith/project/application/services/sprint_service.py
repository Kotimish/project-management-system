from datetime import date

from monolith.project.application.dto import sprint as dto
from monolith.project.application.dto.sprint import UpdateSprintCommand
from monolith.project.application.interfaces.factories.sprint_factory import ISprintFactory
from monolith.project.application.interfaces.services.sprint_service import ISprintService
from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.domain.exceptions.sprint_exception import SprintUnauthorizedError
from monolith.project.domain.interfaces.repositories.sprint_repository import ISprintRepository
from monolith.project.domain.exceptions import sprint_exception


class SprintService(ISprintService):
    """Интерфейс сервиса Спринта"""

    def __init__(
            self,
            factory: ISprintFactory,
            repository: ISprintRepository,
            task_service: ITaskService
    ):
        self.factory = factory
        self.repository = repository
        self.task_service = task_service

    async def create_sprint(self, name: str, project_id: int, start_date: date, end_date: date) -> dto.SprintDTO:
        sprint = self.factory.create(name, project_id, start_date, end_date)
        sprint = await self.repository.add(sprint)
        return dto.SprintDTO(
            id=sprint.id,
            name=sprint.name,
            project_id=sprint.project_id,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
        )

    async def get_sprint_by_id(self, sprint_id: int) -> dto.SprintDTO:
        sprint = await self.repository.get_by_id(sprint_id)
        return dto.SprintDTO(
            id=sprint.id,
            name=sprint.name,
            project_id=sprint.project_id,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
        )

    async def get_all_sprint_by_project_id(self, project_id: int) -> list[dto.SprintDTO]:
        sprints = await self.repository.get_all_by_project_id(project_id)
        return [
            dto.SprintDTO(
                id=sprint.id,
                name=sprint.name,
                project_id=sprint.project_id,
                start_date=sprint.start_date,
                end_date=sprint.end_date,
            )
            for sprint in sprints
        ]

    async def update_sprint(self, project_id: int, sprint_id: int, data: UpdateSprintCommand) -> dto.SprintDTO:
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
        return dto.SprintDTO(
            id=sprint.id,
            name=sprint.name,
            project_id=sprint.project_id,
            start_date=sprint.start_date,
            end_date=sprint.end_date,
        )

    async def delete_sprint(self, project_id: int, sprint_id: int) -> None:
        tasks = await self.task_service.get_list_tasks_by_sprint(sprint_id)
        if len(tasks) > 0:
            raise sprint_exception.SprintCannotBeDeletedException(
                "Sprint has tasks in the project"
            )
        status = await self.repository.remove(sprint_id)
        if not status:
            raise sprint_exception.SprintNotFoundError(
                "Sprint not found in the project"
            )