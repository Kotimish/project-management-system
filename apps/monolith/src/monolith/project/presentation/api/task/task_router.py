from fastapi import APIRouter, Depends, HTTPException

from monolith.project.application.interfaces.services.task_service import ITaskService
from monolith.project.application.interfaces.services.view_service import IViewService
from monolith.project.presentation.api.dependencies import get_view_service
from monolith.project.presentation.api.task.dependencies import get_task_service
from monolith.project.presentation.schemas.task import CreateTaskRequest, TaskResponse, UpdateTaskRequest
from monolith.project.presentation.schemas.views import TaskView
from monolith.project.application.dto import task as task_dto
from monolith.project.domain.exceptions import task_exception as exceptions

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
    return TaskResponse(**task.model_dump())


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
    return TaskResponse(**task.model_dump())


@router.delete("/{task_id}")
async def delete_task(
    project_id: int,
    sprint_id: int,
    task_id: int,
    task_service: ITaskService = Depends(get_task_service)
):
    try:
        await task_service.delete_task(project_id, sprint_id, task_id)
    except exceptions.TaskCannotBeDeletedException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.TaskUnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))