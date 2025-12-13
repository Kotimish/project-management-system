from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from pydantic import SecretStr

from monolith.client.application.dtos.user import CreateUserCommand, LoginUserCommand
from monolith.client.application.interfaces.services.client_service import IClientService
from monolith.client.presentation.api.dependencies import get_client_service, get_current_user
from monolith.client.presentation.api.utils import render_message
from monolith.client.presentation.schemas.register import RegistrateUserRequest
from monolith.config.settings import BASE_DIR, settings, Environment

router = APIRouter(
    tags=["Client auth pages"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(
    directory= BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def get_register(
        request: Request,
        current_user: dict = Depends(get_current_user)
):
    """Страница регистрации нового пользователя"""
    if current_user is not None:
        return render_message(
            request,
            message="Вы уже авторизованы в системе.",
            back_url="/",
            button_text="Перейти на главную",
            current_user=current_user,
        )
    context = {
        "request": request,
    }
    return templates.TemplateResponse(
        "register.html",
        context
    )


@router.post("/register", response_class=HTMLResponse, include_in_schema=False)
async def post_register(
        request: Request,
        login: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        service: IClientService = Depends(get_client_service)
):
    """Регистрация нового пользователя"""
    user = CreateUserCommand(
        login=login,
        email=email,
        password=SecretStr(password)
    )
    try:
        response = await service.register(user)
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
async def get_login(
        request: Request,
        current_user: dict = Depends(get_current_user)
):
    """Страница авторизации пользователя"""
    if current_user is not None:
        return render_message(
            request,
            message="Вы уже авторизованы в системе.",
            back_url="/",
            button_text="Перейти на главную",
            current_user=current_user
        )
    context = {
        "request": request,
    }
    return templates.TemplateResponse(
        "login.html",
        context
    )


@router.post("/login", response_class=HTMLResponse, include_in_schema=False)
async def post_login(
        request: Request,
        login: str = Form(...),
        password: str = Form(...),
        service: IClientService = Depends(get_client_service),
):
    """Авторизация пользователя"""
    try:
        session = LoginUserCommand(
            login=login,
            password=SecretStr(password)
        )
        tokens = await service.login(session)
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
