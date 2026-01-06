from monolith.project.application.dto.project import UpdateProjectCommand
from monolith.project.application.interfaces.factories.project_factory import IProjectFactory
from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.application.interfaces.services.project_service import IProjectService
from monolith.project.domain.interfaces.repositories.project_repository import IProjectRepository
from monolith.project.domain.model import Project, Participant


class ProjectService(IProjectService):
    """Реализация сервиса проектов"""
    def __init__(
            self,
            participant_service: IParticipantService,
            factory: IProjectFactory,
            repository: IProjectRepository
    ):
        self.participant_service = participant_service
        self.factory = factory
        self.repository = repository

    async def create_project(self, name: str, owner_id: int, description: str = None) -> Project:
        project = self.factory.create(name, owner_id, description)
        project = await self.repository.add(project)
        # Добавляем владельца как первого участника
        await self.participant_service.add_participant(
            project_id=project.id,
            user_id=owner_id
        )
        return project

    async def get_project_by_id(self, project_id: int) -> Project:
        return await self.repository.get_by_id(project_id)

    async def get_list_projects_with_user(self, user_id: int) -> list[Project]:
        return await self.repository.get_by_participant_id(user_id)

    async def update_project(self, project_id: int, data: UpdateProjectCommand) -> Project:
        # TODO требуется проверка на владельца проекта
        project = await self.repository.get_by_id(project_id)
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        project.touch()
        project = await self.repository.update(project_id, project)
        return project

    async def delete_project(self, project_id: int) -> bool:
        # TODO требуется проверка на владельца проекта
        return await self.repository.remove(project_id)

    async def add_participant_to_project(self, project_id: int, user_id: int) -> Participant:
        # TODO требуется проверка на владельца проекта
        return await self.participant_service.add_participant(project_id, user_id)

    async def remove_participant_from_project(self, project_id: int, user_id: int) -> bool:
        # TODO требуется проверка на владельца проекта
        return await self.participant_service.remove_participant(project_id, user_id)
