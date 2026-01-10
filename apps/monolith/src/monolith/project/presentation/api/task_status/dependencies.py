from fastapi import Depends

from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.application.services.task_status_service import TaskStatusService
from monolith.project.presentation.api.dependencies import get_task_status_repository


def get_task_status_service(
        repository=Depends(get_task_status_repository)
) -> ITaskStatusService:
    return TaskStatusService(
        repository=repository
    )
