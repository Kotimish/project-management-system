from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import task as task_dto
from monolith.client.application.dtos import user_profile as profile_dto
from monolith.client.application.exceptions import api_client_exception as exceptions
from monolith.client.application.interfaces.services.composite import IProjectTeamService
from monolith.client.application.interfaces.services.sprint_service import ISprintService
from monolith.client.application.interfaces.services.task_service import ITaskService
from monolith.client.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.presentation.api.dependencies import get_current_user, get_participant_with_profile_service, \
    get_user_profile_service
from monolith.client.presentation.api.project import breadcrumbs as project_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_task_service, get_sprint_service, \
    get_task_status_service
from monolith.client.presentation.api.utils import render_message
from monolith.client.presentation.schemas import user_profile as profile_schemas
from monolith.client.presentation.schemas import views
from monolith.client.presentation.schemas.task import CreateTaskSchema, UpdateTaskSchema
from monolith.config.settings import BASE_DIR

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks pages"]
)

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/by_auth_user_id/{auth_user_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_tasks(
        request: Request,
        auth_user_id: int,
        service: ITaskService = Depends(get_task_service),
        current_user: profile_dto.UserProfileDTO = Depends(get_current_user),
):
    raw_task_view = await service.get_tasks_by_auth_user_id(auth_user_id)
    task_view = views.TaskListView.model_validate(raw_task_view.model_dump())

    breadcrumbs = project_breadcrumbs.get_tasks_by_user_breadcrumbs()
    context = {
        "request": request,
        "tasks": task_view.tasks,
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "task/task_list.html",
        context
    )



