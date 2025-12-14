from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.domain.interfaces.repositories.task_status_repository import ITaskStatusRepository
from monolith.project.domain.model import TaskStatus

DEFAULT_SLUG = "pending"


class TaskStatusService(ITaskStatusService):
    """Реализация сервиса статутов задач"""

    def __init__(self, repository: ITaskStatusRepository):
        self.repository = repository

    async def get_all_statuses(self) -> list[TaskStatus]:
        return await self.repository.get_all()

    async def get_status_by_id(self, status_id) -> TaskStatus | None:
        return await self.repository.get_by_id(status_id)

    async def get_status_by_slug(self, slug: str) -> TaskStatus | None:
        return await self.repository.get_by_slug(slug)

    async def get_default_status(self) -> TaskStatus | None:
        return await self.get_status_by_slug(DEFAULT_SLUG)
