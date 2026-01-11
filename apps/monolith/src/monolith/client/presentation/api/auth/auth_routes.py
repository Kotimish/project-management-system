from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from pydantic import SecretStr

from monolith.client.application.dtos.user import CreateUserCommand, LoginUserCommand
from monolith.client.application.interfaces.services.client_service import IClientService
from monolith.client.presentation.api.auth import breadcrumbs as auth_breadcrumbs
from monolith.client.presentation.api.dependencies import get_client_service
from monolith.client.presentation.api.utils import render_message, get_current_user
from monolith.client.application.dtos import user_profile as dto
from monolith.client.presentation.schemas import user_profile as schemas
from monolith.client.presentation.schemas.breadcrumb import Breadcrumb
from monolith.config.settings import BASE_DIR, settings, Environment
from monolith.client.application.exceptions import auth_exception as exceptions

router = APIRouter(
    tags=["Client auth pages"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def get_register_page(
        request: Request,
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница регистрации нового пользователя"""
    if current_user is not None:
        schema = schemas.GetUserProfileResponse(**current_user.model_dump())
        return render_message(
            request,
            message="Вы уже авторизованы в системе.",
            back_url="/",
            button_text="Перейти на главную",
            current_user=schema.model_dump(),
        )
    breadcrumbs = auth_breadcrumbs.get_auth_register_breadcrumbs()
    context = {
        "request": request,
        "breadcrumbs": breadcrumbs
    }
    return templates.TemplateResponse(
        "register.html",
        context
    )


@router.post("/register", response_class=HTMLResponse, include_in_schema=False)
async def post_register(
        request: Request,
        login: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        service: IClientService = Depends(get_client_service)
):
    """Регистрация нового пользователя"""
    user = CreateUserCommand(
        login=login,
        email=email,
        password=SecretStr(password)
    )
    try:
        await service.register(user)
    except exceptions.InvalidAuthLoginException:
        return render_message(
            request,
            message=(
                "Некорректный формат логина. "
                "Логин должен быть без пробелов и спецсимволов."
            ),
            back_url="/register",
            button_text="Вернуться на страницу регистрации",
        )
    except exceptions.InvalidAuthEmailException:
        return render_message(
            request,
            message="Некорректный формат email.",
            back_url="/register",
            button_text="Вернуться на страницу регистрации",
        )
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url="/register",
            button_text="Вернуться на страницу регистрации",
        )
    return render_message(
        request,
        message="Ваш аккаунт создан. Теперь вы можете войти.",
        back_url="/login",
        button_text="Перейти на страницу входа",
    )


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def get_login_page(
        request: Request,
        current_user: dto.UserProfileDTO = Depends(get_current_user)
):
    """Страница авторизации пользователя"""
    if current_user is not None:
        schema = schemas.GetUserProfileResponse(**current_user.model_dump())
        return render_message(
            request,
            message="Вы уже авторизованы в системе.",
            back_url="/",
            button_text="Перейти на главную",
            current_user=schema.model_dump()
        )
    breadcrumbs = auth_breadcrumbs.get_auth_login_breadcrumbs()
    context = {
        "request": request,
        "breadcrumbs": breadcrumbs,
    }
    return templates.TemplateResponse(
        "login.html",
        context
    )


@router.post("/login", response_class=HTMLResponse, include_in_schema=False)
async def post_login(
        request: Request,
        login: Annotated[str, Form()],
        password: Annotated[str, Form()],
        service: IClientService = Depends(get_client_service),
):
    """Авторизация пользователя"""
    try:
        session = LoginUserCommand(
            login=login,
            password=SecretStr(password)
        )
        tokens = await service.login(session)
    except exceptions.AuthUnauthorizedException:
        return render_message(
            request,
            message="Некорректная комбинация логина и пароля.",
            back_url="/login",
            button_text="Вернуться на страницу входа",
        )
    except Exception as e:
        return render_message(
            request,
            message=str(e),
            back_url="/login",
            button_text="Вернуться на страницу входа",
        )
    response = render_message(
        request,
        message=f"Вы успешно вошли в систему под логином \"{login}\".",
        back_url="/",
        button_text="Перейти на главную страницу",
        # Заглушка
        current_user={
            "sub": "Тестовый пользователь"
        }
    )
    if settings.env == Environment.PRODUCTION:
        secure = True
    else:
        secure = False
    response.set_cookie("access_token", tokens.access_token, httponly=True, secure=secure)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True, secure=secure)
    return response


@router.get("/logout", response_class=HTMLResponse, include_in_schema=False)
async def logout(
        request: Request,
        service: IClientService = Depends(get_client_service)
):
    """Запрос на выход пользователя из сессии"""
    refresh_token = request.cookies.get("refresh_token")
    status = await service.logout(refresh_token)
    if not status:
        return render_message(
            request,
            message=f"Произошла ошибка выхода из сессии. Принудительное завершение сессии.",
            back_url="/",
            button_text="Перейти на страницу входа",
        )
    response = RedirectResponse(url="/", status_code=303)
    # Удаляем токены
    if settings.env == Environment.PRODUCTION:
        secure = True
    else:
        secure = False
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=secure,
        httponly=True,
        samesite="lax"
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        secure=secure,
        httponly=True,
        samesite="lax"
    )
    return response
