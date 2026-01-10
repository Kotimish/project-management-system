from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.dtos.project import CreateProjectDTO, UpdateProjectDTO
from monolith.client.application.exceptions import api_client_exception as api_exceptions
from monolith.client.application.exceptions import project_exception as exceptions
from monolith.client.application.interfaces.services.project_service import IProjectService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.presentation.api.dependencies import get_current_user, get_user_profile_service
from monolith.client.presentation.api.project import breadcrumbs as project_breadcrumbs
from monolith.client.presentation.api.project.dependencies import get_project_service
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


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_list_projects(
        request: Request,
        project_service: IProjectService = Depends(get_project_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница списков проектов"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    # Явно указываем на id из сервиса авторизации - auth_user_id
    try:
        projects = await project_service.get_projects_by_user_id(current_user.auth_user_id)
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url="/",
            button_text="Вернуться на главную страницу",
        )

    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_projects_breadcrumbs()
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Список проектов",
        "projects": projects,
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "project/projects_list.html",
        context
    )


@router.get("/create", response_class=HTMLResponse, include_in_schema=False)
async def create_project_page(
        request: Request,
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Страница создания проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_project_create_breadcrumbs()
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Создание проекта",
        "breadcrumbs": breadcrumbs,
        "errors": None,
    }
    return templates.TemplateResponse(
        "project/create_project.html",
        context
    )


@router.post("/create", response_class=HTMLResponse, include_in_schema=False)
async def create_project(
        request: Request,
        name: Annotated[str, Form()],
        description: Annotated[str, Form()] = None,
        project_service: IProjectService = Depends(get_project_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Запрос создания проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    create_project_dto = CreateProjectDTO(
        name=name,
        description=description,
        owner_id=current_user.auth_user_id
    )
    try:
        project = await project_service.create_project(create_project_dto)
    except Exception as e:
        return render_message(
            request,
            message="Что-то пошло не так:" + str(e),
            back_url="/projects/create",
            button_text="Вернуться на страницу создания проекта",
        )
    if project is None:
        return render_message(
            request,
            message="Возникла ошибка при создании нового проекта",
            back_url="/projects/create",
            button_text="Вернуться на страницу создания проекта",
        )
    return RedirectResponse(
        url=f"/projects/{project.id}",
        status_code=303
    )


@router.get("/{project_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def update_project_page(
        request: Request,
        project_id: int,
        project_service: IProjectService = Depends(get_project_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница редактирования проекта"""
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
            back_url=f"/projects/{project_id}",
            button_text="Вернуться на страницу проекта",
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_project_edit_breadcrumbs(
        views.ProjectReference(
            id=project_view.project.id,
            name=project_view.project.name
        )
    )
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Редактирование проекта",
        "project": project_view.project,
        "breadcrumbs": breadcrumbs,
        "errors": None
    }
    return templates.TemplateResponse(
        "project/update_project.html",
        context
    )


@router.post("/{project_id}/edit", response_class=HTMLResponse, include_in_schema=False)
async def update_project(
        request: Request,
        project_id: int,
        name: Annotated[str, Form()],
        description: Annotated[str, Form()] = None,
        project_service: IProjectService = Depends(get_project_service),
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

    create_project_dto = UpdateProjectDTO(
        name=name,
        description=description
    )
    try:
        project = await project_service.update_project(
            project_id,
            create_project_dto
        )
    except Exception as e:
        return render_message(
            request,
            message="Что-то пошло не так:" + str(e),
            back_url=f"/projects/{project_id}/edit",
            button_text="Вернуться на страницу редактирования проекта",
        )
    if project is None:
        return render_message(
            request,
            message="Не удалось обновить проект.",
            back_url=f"/projects/{project_id}/edit",
            button_text="Вернуться на страницу редактирования проекта",
        )
    return RedirectResponse(
        url=f"/projects/{project_id}",
        status_code=303
    )


@router.post("/{project_id}/delete", response_class=HTMLResponse, include_in_schema=False)
async def delete_project(
        request: Request,
        project_id: int,
        project_service: IProjectService = Depends(get_project_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user),
):
    """Запрос на удаление проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    back_url = f"/projects/{project_id}"
    try:
        await project_service.delete_project(project_id)
        return RedirectResponse(url="/projects", status_code=303)
    except exceptions.ProjectCannotBeDeletedException:
        return render_message(
            request=request,
            message="Невозможно удалить проект: есть активные спринты.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к проекту",
            current_user=schema.model_dump()
        )
    except exceptions.ProjectNotFoundError:
        return render_message(
            request=request,
            message="Проект не найден в системе.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к проекту",
            current_user=schema.model_dump()
        )
    except api_exceptions.HTTPStatusError as e:
        return render_message(
            request=request,
            message="Произошла ошибка при удалении проекта.",
            title="Ошибка",
            back_url=back_url,
            button_text="Назад к проекту",
            current_user=schema.model_dump()
        )


@router.get("/{project_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_project_by_id(
        request: Request,
        project_id: int,
        project_service: IProjectService = Depends(get_project_service),
        profile_service: IUserProfileService = Depends(get_user_profile_service),
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница проекта"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    # Явно указываем на id из сервиса авторизации - auth_user_id
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
    if project_view and project_view.project:
        owner = await profile_service.get_profile_by_auth_user_id(project_view.project.owner_id)
    else:
        owner = None
    participants = await profile_service.get_profiles_by_auth_user_ids(project_view.participant_ids)

    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    breadcrumbs = project_breadcrumbs.get_project_detail_breadcrumbs(
        views.ProjectReference(
            id=project_view.project.id,
            name=project_view.project.name
        )
    )
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Проект",
        "project": project_view.project,
        "sprints": project_view.sprints,
        "participants": participants,
        "owner": owner,
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "project/project_detail.html",
        context
    )
