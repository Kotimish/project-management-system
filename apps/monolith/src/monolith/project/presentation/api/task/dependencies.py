from fastapi import Depends

from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.application.services.task_service import TaskService
from monolith.project.infrastructure.factories.task_factory import TaskFactory
from monolith.project.presentation.api.dependencies import get_task_repository
from monolith.project.presentation.api.task_status.dependencies import get_task_status_service


def get_task_service(
        repository=Depends(get_task_repository),
        task_status_service=Depends(get_task_status_service)
) -> ITaskService:
    factory = TaskFactory()
    return TaskService(
        repository=repository,
        factory=factory,
        task_status_service=task_status_service
    )
