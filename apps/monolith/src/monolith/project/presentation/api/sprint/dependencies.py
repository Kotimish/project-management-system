from fastapi import Depends

from monolith.project.application.interfaces.services.sprint_service import ISprintService
from monolith.project.application.services.sprint_service import SprintService
from monolith.project.infrastructure.factories.sprint_factory import SprintFactory
from monolith.project.presentation.api.dependencies import get_sprint_repository
from monolith.project.presentation.api.task.dependencies import get_task_service


def get_sprint_service(
        repository=Depends(get_sprint_repository),
        task_service=Depends(get_task_service),
) -> ISprintService:
    factory = SprintFactory()
    return SprintService(
        repository=repository,
        factory=factory,
        task_service=task_service,
    )
