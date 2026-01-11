from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.exceptions import api_client_exception as exceptions
from monolith.client.application.interfaces.services.project_service import IProjectService
from monolith.client.application.interfaces.services.task_service import ITaskService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.presentation.api.dependencies import get_current_user, get_user_profile_service
from monolith.client.presentation.api.profile import breadcrumbs as profile_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_project_service, get_task_service
from monolith.client.presentation.api.utils import render_message, get_status_color
from monolith.client.presentation.schemas import user_profile as schemas
from monolith.client.presentation.schemas.user_profile import UpdateUserProfileRequest
from monolith.config.settings import BASE_DIR

router = APIRouter(
    prefix="/profiles",
    tags=["Client profile pages"]
)

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_user_profiles(
        request: Request,
        profile_service: IUserProfileService = Depends(get_user_profile_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница профиля пользователя"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )

    profiles = await profile_service.get_all_profiles()

    user_schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = profile_breadcrumbs.get_profiles_breadcrumbs()
    context = {
        "request": request,
        "user": user_schema.model_dump(),
        "profiles": profiles,
        "page_title": "Профиль",
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "profile/profile_list.html",
        context
    )


@router.get("/{user_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def get_update_profile_page(
        request: Request,
        user_id: int,
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница профиля пользователя (в режиме редактирования)"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = profile_breadcrumbs.get_profile_edit_breadcrumbs(user_id)
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Профиль",
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "profile/update_profile.html",
        context
    )


@router.post("/{user_id}/update", response_class=HTMLResponse, include_in_schema=False)
async def update_profile(
        request: Request,
        user_id: int,
        data: Annotated[UpdateUserProfileRequest, Form()],
        current_user: dto.UserProfileDTO = Depends(get_current_user),
        profile_service: IUserProfileService = Depends(get_user_profile_service)
):
    """Запрос на обновление профиля"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    update_dto = dto.UpdateUserProfileCommand.model_validate(data.model_dump())
    access_token = request.cookies.get("access_token")
    await profile_service.update_profile(
        current_user.id,
        update_dto,
        access_token
    )
    return RedirectResponse(url=f"/profiles/{user_id}", status_code=303)


@router.get("/{user_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_user_profile(
        request: Request,
        user_id: int,
        profile_service: IUserProfileService = Depends(get_user_profile_service),
        project_service: IProjectService = Depends(get_project_service),
        task_service: ITaskService = Depends(get_task_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница профиля пользователя"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )

    profile = await profile_service.get_profile_by_auth_user_id(user_id)
    profile_schema = schemas.GetUserProfileResponse(**profile.model_dump())

    try:
        projects = await project_service.get_projects_by_user_id(user_id)
    except exceptions.HTTPStatusError:
        projects = []

    try:
        tasks_view = await task_service.get_tasks_by_auth_user_id(user_id)
        tasks = tasks_view.tasks if tasks_view else []
    except exceptions.HTTPStatusError:
        tasks = []

    colored_tasks = [
        {
            **task.model_dump(),
            'color': get_status_color(task.status.slug)
        }
        for task in tasks
    ]

    user_schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = profile_breadcrumbs.get_profile_breadcrumbs(user_id)
    context = {
        "request": request,
        "user": user_schema.model_dump(),
        "profile": profile_schema.model_dump(),
        "projects": projects,
        "tasks": colored_tasks,
        "page_title": "Профиль",
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "profile/user_profile_detail.html",
        context
    )
