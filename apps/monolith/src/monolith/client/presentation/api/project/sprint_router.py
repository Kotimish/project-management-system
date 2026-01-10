from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.dtos.sprint import CreateSprintCommand, UpdateSprintCommand
from monolith.client.application.interfaces.services.project_service import IProjectService
from monolith.client.application.interfaces.services.sprint_service import ISprintService
from monolith.client.presentation.api.dependencies import get_current_user
from monolith.client.presentation.api.project import breadcrumbs as project_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_sprint_service, get_project_service
from monolith.client.presentation.api.utils import render_message, get_status_color
from monolith.client.presentation.schemas import user_profile as schemas
from monolith.client.presentation.schemas import views
from monolith.config.settings import BASE_DIR

router = APIRouter(
    prefix="/projects/{project_id}/sprints",
    tags=["Sprints pages"]
)

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_sprints_by_project_id(
        request: Request,
        project_id: int,
        service: ISprintService = Depends(get_sprint_service),
        project_service: IProjectService = Depends(get_project_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница списков проектов"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    try:
        sprints = await service.get_sprints_by_project_id(project_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}",
            button_text="Вернуться на страницу проекта",
        )
    try:
        project_view = await project_service.get_project_by_id(project_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}",
            button_text="Вернуться на страницу проекта",
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_sprints_breadcrumbs(
        views.ProjectReference(
            id=project_view.project.id,
            name=project_view.project.name
        )
    )
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Список спринтов",
        "sprints": sprints,
        "project": project_view.project,
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "sprint/sprint_list.html",
        context
    )


@router.get("/create", response_class=HTMLResponse, include_in_schema=False)
async def create_sprint_page(
        request: Request,
        project_id: int,
        project_service: IProjectService = Depends(get_project_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница создания спринта в проекте"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    try:
        project_view = await project_service.get_project_by_id(project_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints",
            button_text="Вернуться на список спринтов",
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_sprints_breadcrumbs(
        views.ProjectReference(
            id=project_view.project.id,
            name=project_view.project.name
        )
    )
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Создание спринта",
        "project": project_view.project,
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "sprint/create_sprint.html",
        context
    )


@router.post("/create", response_class=HTMLResponse, include_in_schema=False)
async def create_sprint(
        request: Request,
        project_id: int,
        name: Annotated[str, Form()],
        start_date: Annotated[date, Form()],
        end_date: Annotated[date, Form()],
        service: ISprintService = Depends(get_sprint_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Запрос создания спринта в проекте"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    create_sprint_dto = CreateSprintCommand(
        name=name,
        start_date=start_date,
        end_date=end_date,
    )
    try:
        sprint = await service.create_sprint(project_id, create_sprint_dto)
    except Exception as e:
        return render_message(
            request,
            message="Что-то пошло не так:" + str(e),
            back_url=f"/projects/{project_id}/sprints/create",
            button_text="Вернуться на страницу создания спринта",
        )
    if sprint is None:
        return render_message(
            request,
            message="Возникла ошибка при создании нового спринта",
            back_url=f"/projects/{project_id}/sprints/create",
            button_text="Вернуться на страницу создания спринта",
        )

    return RedirectResponse(
        url=f"/projects/{project_id}/sprints/{sprint.id}",
        status_code=303
    )


@router.get("/{sprint_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def update_project_page(
        request: Request,
        project_id: int,
        sprint_id: int,
        service: ISprintService = Depends(get_sprint_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
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
        sprint_view = await service.get_sprint_by_id(project_id, sprint_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}/sprints/{project_id}",
            button_text="Вернуться на страницу спринта",
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_sprint_update_breadcrumbs(
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
        "user": schema.model_dump(),
        "page_title": "Редактирование спринта",
        "sprint": sprint_view.sprint,
        "project": sprint_view.project,
        "breadcrumbs": breadcrumbs,
        "errors": None
    }
    return templates.TemplateResponse(
        "sprint/update_sprint.html",
        context
    )


@router.post("/{sprint_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def update_sprint(
        request: Request,
        project_id: int,
        sprint_id: int,
        name: Annotated[str, Form()],
        start_date: Annotated[date, Form()],
        end_date: Annotated[date, Form()],
        service: ISprintService = Depends(get_sprint_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Запрос на редактирование проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )

    update_sprint_dto = UpdateSprintCommand(
        name=name,
        start_date=start_date,
        end_date=end_date,
    )
    try:
        sprint = await service.update_sprint(
            project_id,
            sprint_id,
            update_sprint_dto
        )
    except Exception as e:
        return render_message(
            request,
            message="Что-то пошло не так:" + str(e),
            back_url=f"/projects/{project_id}/sprints/{sprint_id}/edit",
            button_text="Вернуться на страницу редактирования спринта",
        )
    if sprint is None:
        return render_message(
            request,
            message="Не удалось обновить спринт.",
            back_url=f"/projects/{project_id}/sprints/{sprint_id}/edit",
            button_text="Вернуться на страницу редактирования спринта",
        )
    return RedirectResponse(
        url=f"/projects/{project_id}/sprints/{sprint_id}",
        status_code=303
    )


@router.get("/{sprint_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_sprint_by_id(
        request: Request,
        project_id: int,
        sprint_id: int,
        service: ISprintService = Depends(get_sprint_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница спринта проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    try:
        sprint_view = await service.get_sprint_by_id(project_id, sprint_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url=f"/projects/{project_id}",
            button_text="Вернуться на страницу списка спринтов",
        )

    if sprint_view is None:
        return render_message(
            request,
            message="Указанный спринт не найден или у вас отсутствуют права доступа к нему.",
            back_url=f"/projects/{project_id}",
            button_text="Перейти на страницу списка спринтов"
        )

    colored_tasks = [
        {
            **task.model_dump(),
            'color': get_status_color(task.status.slug)
        }
        for task in sprint_view.tasks
    ]

    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_sprint_detail_breadcrumbs(
        views.ProjectReference(
            id=sprint_view.project.id,
            name=sprint_view.project.name,
        ),
        views.SprintReference(
            id=sprint_view.sprint.id,
            name=sprint_view.sprint.name,
        ),
    )
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Спринт",
        "sprint": sprint_view.sprint,
        "project": sprint_view.project,
        "tasks": colored_tasks,
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "sprint/sprint_detail.html",
        context
    )
