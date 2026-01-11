from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.exceptions import api_client_exception as api_exceptions
from monolith.client.application.exceptions import participant_exception as exceptions
from monolith.client.application.interfaces.services.participant_service import IParticipantService
from monolith.client.application.interfaces.services.project_service import IProjectService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.presentation.api.dependencies import get_current_user, get_user_profile_service
from monolith.client.presentation.api.project import breadcrumbs as project_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_project_service, get_participant_service
from monolith.client.presentation.api.utils import render_message
from monolith.client.presentation.schemas import user_profile as schemas
from monolith.client.presentation.schemas import views
from monolith.config.settings import BASE_DIR

router = APIRouter(
    prefix="/projects",
    tags=["Projects pages"]
)

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/{project_id}/participants/edit", response_class=HTMLResponse, include_in_schema=False)
async def get_project_participants_page(
        request: Request,
        project_id: int,
        project_service: IProjectService = Depends(get_project_service),
        profile_service: IUserProfileService = Depends(get_user_profile_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница списка участников проектов"""
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
            back_url="/projects",
            button_text="Вернуться на страницу списка проектов",
        )

    if project_view is None:
        return render_message(
            request,
            message="Указанный проект не найден или у вас отсутствуют права доступа к нему.",
            back_url="/projects",
            button_text="Перейти на страницу списка проектов"
        )

    project_view = await project_service.get_project_by_id(project_id)
    if project_view and project_view.project:
        owner = await profile_service.get_profile_by_auth_user_id(project_view.project.owner_id)
    else:
        owner = None
    participants = await profile_service.get_profiles_by_auth_user_ids(project_view.participant_ids)
    participant_ids_set = set(project_view.participant_ids)
    users = await profile_service.get_all_profiles()
    users = [
        user
        for user in users
        if user.auth_user_id not in participant_ids_set
    ]

    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_project_edit_participants_breadcrumbs(
        views.ProjectReference(
            id=project_view.project.id,
            name=project_view.project.name
        )
    )
    context = {
        "request": request,
        "page_title": "Управление командой",
        "user": schema.model_dump(),
        "project": project_view.project,
        "breadcrumbs": breadcrumbs,
        "owner": owner,
        "participants": participants,
        "users": users,
        "errors": None,
    }
    return templates.TemplateResponse(
        "project/update_participant_list.html",
        context
    )


@router.post("/{project_id}/participants/{user_id}/add", response_class=HTMLResponse, include_in_schema=False)
async def add_participant_to_project(
        request: Request,
        project_id: int,
        user_id: int,
        participant_service: IParticipantService = Depends(get_participant_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    access_token = request.cookies.get("access_token")
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    try:
        await participant_service.add_participant_to_project(project_id, user_id, access_token)
        return RedirectResponse(url=f"/projects/{project_id}/participants/edit", status_code=303)
    except exceptions.ParticipantForbiddenException:
        return render_message(
            request=request,
            message="Только владелец проекта может редактировать список участников проекта.",
            title="Ошибка",
            back_url=f"/projects/{project_id}/participants/edit",
            button_text="Назад к странице редактирования участников",
            current_user=schema.model_dump()
        )


@router.post("/{project_id}/participants/{user_id}/remove", response_class=HTMLResponse, include_in_schema=False)
async def remove_participant_from_project(
        request: Request,
        project_id: int,
        user_id: int,
        participant_service: IParticipantService = Depends(get_participant_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    access_token = request.cookies.get("access_token")
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    back_url = f"/projects/{project_id}/participants/edit"
    try:
        await participant_service.remove_participant_from_project(project_id, user_id, access_token)
        return RedirectResponse(url=back_url, status_code=303)
    except exceptions.ParticipantCannotBeDeletedException:
        return render_message(
            request=request,
            message="Невозможно удалить участника: у него есть задачи в проекте.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к участникам",
            current_user=schema.model_dump()
        )
    except exceptions.ParticipantNotFoundError:
        return render_message(
            request=request,
            message="Участник не найден в команде проекта.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к участникам",
            current_user=schema.model_dump()
        )
    except exceptions.ParticipantForbiddenException:
        return render_message(
            request=request,
            message="Только владелец проекта может редактировать список участников проекта.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к участникам",
            current_user=schema.model_dump()
        )
    except api_exceptions.HTTPStatusError as e:
        return render_message(
            request=request,
            message="Произошла ошибка при удалении участника.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к участникам",
            current_user=schema.model_dump()
        )
