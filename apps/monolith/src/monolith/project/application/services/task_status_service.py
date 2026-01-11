from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.domain.interfaces.repositories.task_status_repository import ITaskStatusRepository
from monolith.project.domain.model import TaskStatus
from monolith.project.application.dto import task_status as dto

DEFAULT_SLUG = "pending"


class TaskStatusService(ITaskStatusService):
    """Реализация сервиса статутов задач"""

    def __init__(self, repository: ITaskStatusRepository):
        self.repository = repository

    async def get_all_statuses(self) -> list[dto.TaskStatusDTO]:
        statuses = await self.repository.get_all()
        return [
            dto.TaskStatusDTO(
                id=status.id,
                name=status.name,
                slug=status.slug,
                description=status.description
            )
            for status in statuses
        ]

    async def get_status_by_id(self, status_id) -> dto.TaskStatusDTO | None:
        status = await self.repository.get_by_id(status_id)
        return dto.TaskStatusDTO(
            id=status.id,
            name=status.name,
            slug=status.slug,
            description=status.description
        )

    async def get_status_by_slug(self, slug: str) -> dto.TaskStatusDTO | None:
        status = await self.repository.get_by_slug(slug)
        return dto.TaskStatusDTO(
            id=status.id,
            name=status.name,
            slug=status.slug,
            description=status.description
        )

    async def get_default_status(self) -> dto.TaskStatusDTO | None:
        status = await self.get_status_by_slug(DEFAULT_SLUG)
        return dto.TaskStatusDTO(**status.model_dump())
