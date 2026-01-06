from fastapi import APIRouter, Depends

from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.application.interfaces.services.view_service import IViewService
from monolith.project.presentation.api.dependencies import get_task_service, get_view_service
from monolith.project.presentation.schemas.task import CreateTaskRequest, TaskResponse, UpdateTaskRequest
from monolith.project.presentation.schemas.views import TaskView
from monolith.project.application.dto import task as task_dto

router = APIRouter(
    prefix="/projects/{project_id}/sprints/{sprint_id}/tasks",
    tags=["task"]
)


@router.post("/", response_model=TaskResponse)
async def create_task(
    project_id: int,
    sprint_id: int,
    data: CreateTaskRequest,
    service: ITaskService = Depends(get_task_service)
):
    task = await service.create_task(
        data.title,
        project_id,
        data.assignee_id,
        sprint_id,
        data.description
    )
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        status_id=task.status_id,
        assignee_id=task.assignee_id,
        sprint_id=task.sprint_id,
    )


@router.get("/{task_id}", response_model=TaskView)
async def get_task(
    project_id: int,
    sprint_id: int,
    task_id: int,
    service: IViewService = Depends(get_view_service)
):
    task = await service.get_task_detail(project_id, sprint_id, task_id)
    return TaskView(**task.model_dump())


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    project_id: int,
    sprint_id: int,
    task_id: int,
    data: UpdateTaskRequest,
    service: ITaskService = Depends(get_task_service)
):
    update_task_dto = task_dto.UpdateTaskCommand(**data.model_dump())
    task = await service.update_task(project_id, sprint_id, task_id, update_task_dto)
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        status_id=task.status_id,
        assignee_id=task.assignee_id,
        sprint_id=task.sprint_id,
    )


@router.delete("/{task_id}")
async def delete_task(
    project_id: int,
    sprint_id: int,
    task_id: int,
    service: ITaskService = Depends(get_task_service)
):
    await service.delete_task(task_id)
