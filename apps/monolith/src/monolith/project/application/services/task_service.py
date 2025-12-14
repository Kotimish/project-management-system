from monolith.project.application.interfaces.factories.task_factory import ITaskFactory
from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.domain.interfaces.repositories.task_repository import ITaskRepository
from monolith.project.domain.model import Task


class TaskService(ITaskService):
    """Реализация сервиса задач"""

    def __init__(
            self,
            task_status_service: ITaskStatusService,
            factory: ITaskFactory,
            repository: ITaskRepository
    ):
        self.task_status_service = task_status_service
        self.factory = factory
        self.repository = repository

    async def create_task(
            self,
            title: str,
            project_id: int,
            assignee_id: int | None = None,
            description: str | None = None
    ) -> Task:
        status = await self.task_status_service.get_default_status()
        task = self.factory.create(title, project_id, status.id, assignee_id, description)
        task = await self.repository.add(task)
        raise task

    async def get_task_by_id(self, task_id: int) -> Task:
        return await self.repository.get_by_id(task_id)

    async def get_list_tasks_by_assignee_id(self, assignee_id: int) -> list[Task]:
        return await self.repository.get_list_tasks_by_assignee(assignee_id)

    async def get_list_tasks_by_project(self, project_id: int) -> list[Task]:
        return await self.repository.get_list_tasks_by_project(project_id)

    async def get_list_tasks_by_sprint(self, sprint_id: int) -> list[Task]:
        return await self.repository.get_list_tasks_by_sprint(sprint_id)

    async def delete_task(self, task_id: int) -> bool:
        return await self.repository.remove(task_id)

    async def assign_task(self, task_id: int, assignee_id: int) -> Task:
        task = await self.repository.get_by_id(task_id)
        task.assignee_id = assignee_id
        task = await self.repository.update(task_id, task)
        return task

    async def update_task_status(self, task_id: int, status_id: int) -> Task:
        task = await self.repository.get_by_id(task_id)
        task.status_id = status_id
        task = await self.repository.update(task_id, task)
        return task

    async def add_task_to_sprint(self, task_id: int, sprint_id: int) -> Task:
        task = await self.repository.get_by_id(task_id)
        task.sprint_id = sprint_id
        task = await self.repository.update(task_id, task)
        return task
