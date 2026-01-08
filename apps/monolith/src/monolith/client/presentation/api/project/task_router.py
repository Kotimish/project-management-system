from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import task as task_dto
from monolith.client.application.dtos import user_profile as profile_dto
from monolith.client.application.interfaces.services.composite import IProjectTeamService
from monolith.client.application.interfaces.services.participant_service import IParticipantService
from monolith.client.application.interfaces.services.sprint_service import ISprintService
from monolith.client.application.interfaces.services.task_service import ITaskService
from monolith.client.application.interfaces.services.task_status_service import ITaskStatusService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.presentation.api.dependencies import get_current_user, get_participant_with_profile_service, \
    get_user_profile_service
from monolith.client.presentation.api.project import breadcrumbs as project_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_task_service, get_sprint_service, \
    get_task_status_service, get_participant_service
from monolith.client.presentation.api.utils import render_message
from monolith.client.presentation.schemas import user_profile as profile_schemas
from monolith.client.presentation.schemas import views
from monolith.client.presentation.schemas.task import CreateTaskSchema, UpdateTaskSchema
from monolith.config.settings import BASE_DIR

router = APIRouter(
    prefix="/projects/{project_id}/sprints/{sprint_id}/tasks",
    tags=["Tasks pages"]
)

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/create", response_class=HTMLResponse, include_in_schema=False)
async def create_task_page(
        request: Request,
        project_id: int,
        sprint_id: int,
        sprint_service: ISprintService = Depends(get_sprint_service),
        participant_service: IProjectTeamService = Depends(get_participant_with_profile_service),
        current_user: profile_dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница создания задачи спринта в проекте"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    try:
        sprint_view = await sprint_service.get_sprint_by_id(project_id, sprint_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Вернуться на страницу списка задач",
        )
    try:
        participants = await participant_service.get_participants_by_project(project_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Вернуться на страницу списка задач",
        )

    user_schema = profile_schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_task_create_breadcrumbs(
        views.ProjectReference(
            id=sprint_view.project.id,
            name=sprint_view.project.name
        ),
        views.SprintReference(
            id=sprint_view.sprint.id,
            name=sprint_view.sprint.name
        )
    )
    context = {
        "request": request,
        "user": user_schema.model_dump(),
        "page_title": "Создание задачи",
        "project": sprint_view.project,
        "sprint": sprint_view.sprint,
        "participants": participants,
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "task/create_task.html",
        context
    )


@router.post("/create", response_class=HTMLResponse, include_in_schema=False)
async def create_task(
        request: Request,
        project_id: int,
        sprint_id: int,
        data: Annotated[CreateTaskSchema, Form()],
        service: ITaskService = Depends(get_task_service),
        current_user: profile_dto.UserProfileDTO = Depends(get_current_user),
):
    """Запрос создания задачи спринта в проекте"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    create_task_dto = task_dto.CreateTaskCommand(
        title=data.title,
        description=data.description,
        assignee_id=data.assignee,
    )
    try:
        task = await service.create_task(project_id, sprint_id, create_task_dto)
    except Exception as e:
        return render_message(
            request,
            message="Что-то пошло не так:" + str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}/tasks/create",
            button_text="Вернуться на страницу создания задачи",
        )
    if task is None:
        return render_message(
            request,
            message="Возникла ошибка при создании новой задачи",
            back_url=f"/projects/{project_id}/sprints/{sprint_id}/tasks/create",
            button_text="Вернуться на страницу создания задачи",
        )
    return RedirectResponse(
        url=f"/projects/{project_id}/sprints/{sprint_id}/tasks/{task.id}",
        status_code=303
    )


@router.get("/{task_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def update_task_page(
        request: Request,
        project_id: int,
        sprint_id: int,
        task_id: int,
        task_service: ITaskService = Depends(get_task_service),
        status_service: ITaskStatusService = Depends(get_task_status_service),
        participant_service: IProjectTeamService = Depends(get_participant_with_profile_service),
        current_user: profile_dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница редактирования спринта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url=f"/login",
            button_text="Перейти на страницу входа"
        )
    try:
        task_view = await task_service.get_task_by_id(project_id, sprint_id, task_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Вернуться на страницу списка задач",
        )
    try:
        statuses = await status_service.get_task_statuses()
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Вернуться на страницу списка задач",
        )
    try:
        participants = await participant_service.get_participants_by_project(project_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Вернуться на страницу списка задач",
        )


    schema = profile_schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_sprint_update_breadcrumbs(
        views.ProjectReference(
            id=task_view.project.id,
            name=task_view.project.name
        ),
        views.SprintReference(
            id=task_view.sprint.id,
            name=task_view.sprint.name
        )
    )
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Редактирование спринта",
        "project": task_view.project,
        "sprint": task_view.sprint,
        "task": task_view.task,
        "breadcrumbs": breadcrumbs,
        "statuses": statuses,
        "participants": participants,
        "errors": None
    }
    return templates.TemplateResponse(
        "task/update_task.html",
        context
    )


@router.post("/{task_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def update_task(
        request: Request,
        project_id: int,
        sprint_id: int,
        task_id: int,
        data: Annotated[UpdateTaskSchema, Form()],
        service: ITaskService = Depends(get_task_service),
        current_user: profile_dto.UserProfileDTO = Depends(get_current_user),
):
    """Запрос на редактирование проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )

    update_task_dto = task_dto.UpdateTaskCommand(
        title=data.title,
        status_id=data.status,
        assignee_id=data.assignee,
        description=data.description,
    )
    try:
        task = await service.update_task(
            project_id,
            sprint_id,
            task_id,
            update_task_dto
        )
    except Exception as e:
        return render_message(
            request,
            message="Что-то пошло не так:" + str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}/tasks/{task_id}/edit",
            button_text="Вернуться на страницу редактирования задачи",
        )
    if task is None:
        return render_message(
            request,
            message="Не удалось обновить задачу.",
            back_url=f"/projects/{project_id}/sprints/{sprint_id}/tasks/{task_id}/edit",
            button_text="Вернуться на страницу редактирования задачи",
        )

    return RedirectResponse(
        url=f"/projects/{project_id}/sprints/{sprint_id}/tasks/{task_id}",
        status_code=303
    )


@router.get("/{task_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_task_by_id(
        request: Request,
        project_id: int,
        sprint_id: int,
        task_id: int,
        task_service: ITaskService = Depends(get_task_service),
        profile_service: IUserProfileService = Depends(get_user_profile_service),
        current_user: profile_dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница Задачи"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )

    try:
        task_view = await task_service.get_task_by_id(project_id, sprint_id, task_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Вернуться на страницу списка задач",
        )

    if task_view is None:
        return render_message(
            request,
            message="Указанная задача не найдена или у вас отсутствуют права доступа к ней.",
            back_url=f"/projects/{project_id}/sprints/{sprint_id}",
            button_text="Перейти на страницу списка задач"
        )

    if task_view.task.assignee:
        try:
            profile = await profile_service.get_profile_by_auth_user_id(task_view.task.assignee.auth_user_id)
        except Exception as e:
            return render_message(
                request,
                message=str(e),
                back_url=f"/projects/{project_id}/sprints/{sprint_id}",
                button_text="Вернуться на страницу списка задач",
            )
    else:
        profile = None



    user_schema = profile_schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_task_detail_breadcrumbs(
        views.ProjectReference(
            id=task_view.project.id,
            name=task_view.project.name,
        ),
        views.SprintReference(
            id=task_view.sprint.id,
            name=task_view.sprint.name,
        ),
        views.TaskReference(
            id=task_view.task.id,
            title=task_view.task.title,
        ),
    )
    context = {
        "request": request,
        "user": user_schema.model_dump(),
        "page_title": "Задача",
        "project": task_view.project,
        "sprint": task_view.sprint,
        "task": task_view.task,
        "profile": profile,
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "task/task_detail.html",
        context
    )
