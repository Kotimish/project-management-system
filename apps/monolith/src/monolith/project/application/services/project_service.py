from monolith.project.application.dto import project as project_dto
from monolith.project.application.dto import participant as participant_dto
from monolith.project.application.dto.project import UpdateProjectCommand
from monolith.project.application.interfaces.factories.project_factory import IProjectFactory
from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.application.interfaces.services.project_service import IProjectService
from monolith.project.application.interfaces.services.sprint_service import ISprintService
from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.domain.exceptions import participant_exception
from monolith.project.domain.exceptions import project_exception
from monolith.project.domain.interfaces.repositories.project_repository import IProjectRepository


class ProjectService(IProjectService):
    """Реализация сервиса проектов"""

    def __init__(
            self,
            factory: IProjectFactory,
            repository: IProjectRepository,
            participant_service: IParticipantService,
            task_service: ITaskService,
            sprint_service: ISprintService
    ):
        self.factory = factory
        self.repository = repository
        self.participant_service = participant_service
        self.task_service = task_service
        self.sprint_service = sprint_service

    async def create_project(self, name: str, owner_id: int, description: str = None) -> project_dto.ProjectDTO:
        project = self.factory.create(name, owner_id, description)
        project = await self.repository.add(project)
        # Добавляем владельца как первого участника
        await self.participant_service.add_participant(
            project_id=project.id,
            user_id=owner_id
        )
        return project_dto.ProjectDTO(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    async def get_project_by_id(self, project_id: int) -> project_dto.ProjectDTO:
        project = await self.repository.get_by_id(project_id)
        return project_dto.ProjectDTO(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    async def get_list_projects_with_user(self, user_id: int) -> list[project_dto.ProjectDTO]:
        projects = await self.repository.get_by_participant_id(user_id)
        return [
            project_dto.ProjectDTO(
                id=project.id,
                name=project.name,
                description=project.description,
                owner_id=project.owner_id,
                created_at=project.created_at,
                updated_at=project.updated_at,
            )
            for project in projects
        ]

    async def update_project(self, project_id: int, owner_id: int, data: UpdateProjectCommand) -> project_dto.ProjectDTO:
        project = await self.repository.get_by_id(project_id)
        if project.owner_id != owner_id:
            raise project_exception.ProjectForbiddenError("User do not have permission to modify this resource")

        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        project.touch()
        project = await self.repository.update(project_id, project)
        return project_dto.ProjectDTO(
            id=project.id,
            name=project.name,
            description=project.description,
            owner_id=project.owner_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    async def delete_project(self, project_id: int, owner_id: int) -> None:
        project = await self.repository.get_by_id(project_id)
        if project.owner_id != owner_id:
            raise project_exception.ProjectForbiddenError("User do not have permission to modify this resource")
        sprints = await self.sprint_service.get_all_sprint_by_project_id(project_id)
        if len(sprints) > 0:
            raise project_exception.ProjectCannotBeDeletedException(
                "Project has sprints"
            )
        participants = await self.participant_service.get_participants_by_project(project_id)
        for participant in participants:
            await self.remove_participant_from_project(project_id, owner_id, participant.auth_user_id)
        status = await self.repository.remove(project_id)
        if not status:
            raise project_exception.ProjectNotFoundError(
                "Project not found"
            )

    async def add_participant_to_project(self, project_id: int, owner_id: int, user_id: int) -> participant_dto.ParticipantDTO:
        project = await self.repository.get_by_id(project_id)
        if project.owner_id != owner_id:
            raise project_exception.ProjectForbiddenError("User do not have permission to modify this resource")
        return await self.participant_service.add_participant(project_id, user_id)

    async def remove_participant_from_project(self, project_id: int, owner_id: int, user_id: int) -> None:
        project = await self.repository.get_by_id(project_id)
        if project.owner_id != owner_id:
            raise project_exception.ProjectForbiddenError("User do not have permission to modify this resource")
        tasks = await self.task_service.get_tasks_by_auth_user_in_project(project_id, user_id)
        if len(tasks) > 0:
            raise participant_exception.ParticipantCannotBeDeletedException(
                "Participant has tasks in the project"
            )
        await self.participant_service.remove_participant(project_id, user_id)
