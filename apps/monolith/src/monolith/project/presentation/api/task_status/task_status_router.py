from fastapi import APIRouter, Depends

from monolith.project.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.project.presentation.api.dependencies import get_task_status_service
from monolith.project.presentation.schemas.task_status import TaskStatusResponse

router = APIRouter(
    prefix="/task_status",
    tags=["task_status"]
)


@router.get("/", response_model=list[TaskStatusResponse])
async def get_task_statuses(
        service: ITaskStatusService = Depends(get_task_status_service)
) -> list[TaskStatusResponse]:
    all_statuses = await service.get_all_statuses()
    return [
        TaskStatusResponse(
            name=status.name,
            slug=status.slug,
            description=status.description,
            status_id=status.id,
        )
        for status in all_statuses
    ]


@router.get("/{task_status_id}", response_model=TaskStatusResponse)
async def get_task_status(
        task_status_id: int,
        service: ITaskStatusService = Depends(get_task_status_service)
) -> TaskStatusResponse:
    status = await service.get_status_by_id(task_status_id)
    return TaskStatusResponse(
        name=status.name,
        slug=status.slug,
        description=status.description,
        status_id=status.id,
    )
