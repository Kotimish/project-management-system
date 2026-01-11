from fastapi import APIRouter, Depends, Query

from monolith.project.application.interfaces.services.view_service import IViewService
from monolith.project.presentation.api.dependencies import get_view_service
from monolith.project.presentation.schemas.views import TaskListView

router = APIRouter(
    prefix="/tasks",
    tags=["task"]
)


@router.get("/by_auth_user_id/{auth_user_id}", response_model=TaskListView)
async def get_tasks(
        auth_user_id: int,
        service: IViewService = Depends(get_view_service)
):
    task = await service.get_tasks_by_auth_user_id(auth_user_id)
    return TaskListView.model_validate(task.model_dump())
