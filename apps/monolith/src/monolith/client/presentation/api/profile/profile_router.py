from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from monolith.client.application.dtos import user_profile as dto
from monolith.client.presentation.schemas import user_profile as schemas
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.presentation.api.dependencies import get_current_user, get_user_profile_service
from monolith.client.presentation.api.utils import render_message
from monolith.config.settings import BASE_DIR

router = APIRouter(
    prefix="/profile",
    tags=["Client profile pages"]
)

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def profile(
        request: Request,
        current_user: dto.GetUserProfileResponse = Depends(get_current_user)
):
    """Страница профиля пользователя"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    schema = schemas.GetUserProfileResponse(**current_user.model_dump())
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Профиль",
    }
    return templates.TemplateResponse(
        "user_profile.html",
        context
    )


@router.get("/edit", response_class=HTMLResponse, include_in_schema=False)
async def profile_edit_page(
        request: Request,
        current_user: dto.GetUserProfileResponse = Depends(get_current_user)
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
    context = {
        "request": request,
        "user": schema.model_dump(),
        "page_title": "Профиль",
    }
    return templates.TemplateResponse(
        "user_profile_edit_mode.html",
        context
    )


@router.post("/update", response_class=HTMLResponse, include_in_schema=False)
async def update_profile(
        request: Request,
        display_name: Annotated[str, Form()],
        first_name: Annotated[str | None, Form()] = None,
        middle_name: Annotated[str | None, Form()] = None,
        last_name: Annotated[str | None, Form()] = None,
        description: Annotated[str | None, Form()] = None,
        birthdate: Annotated[date | None, Form()] = None,
        phone: Annotated[str | None, Form()] = None,
        current_user: dto.GetUserProfileResponse = Depends(get_current_user),
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
    update_dto = dto.UpdateUserProfileCommand(
        display_name=display_name,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        description=description,
        birthdate=birthdate,
        phone=phone,
    )
    access_token = request.cookies.get("access_token")
    await profile_service.update_profile(
        current_user.id,
        update_dto,
        access_token
    )
    return RedirectResponse(url="/profile", status_code=303)
