from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from monolith.client.application.dtos import user_profile as profile_dto
from monolith.client.application.interfaces.services.task_service import ITaskService
from monolith.client.presentation.api.dependencies import get_current_user
from monolith.client.presentation.api.project import breadcrumbs as project_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_task_service
from monolith.client.presentation.api.utils import render_message, get_status_color
from monolith.client.presentation.schemas import user_profile as schemas
from monolith.client.presentation.schemas import views
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
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    raw_task_view = await service.get_tasks_by_auth_user_id(auth_user_id)
    task_view = views.TaskListView.model_validate(raw_task_view.model_dump())

    colored_tasks = [
        {
            **task.model_dump(),
            'color': get_status_color(task.status.slug)
        }
        for task in task_view.tasks
    ]
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_tasks_by_user_breadcrumbs()
    context = {
        "request": request,
        "user": schema.model_dump(),
        "tasks": colored_tasks,
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "task/task_list.html",
        context
    )
