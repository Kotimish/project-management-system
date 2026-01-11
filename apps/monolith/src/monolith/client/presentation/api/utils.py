from fastapi import Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.interfaces.services.client_service import IClientService

from monolith.client.presentation.api.constants import STATUS_COLOR_MAP, DEFAULT_COLOR
from monolith.client.presentation.api.dependencies import get_client_service
from monolith.config.settings import BASE_DIR

templates = Jinja2Templates(
    directory=BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)

def get_status_color(status_name: str) -> str:
    """Получить цвет для статуса задачи в шаблоне html-страницы"""
    color = STATUS_COLOR_MAP.get(status_name)
    if color is None:
        return DEFAULT_COLOR
    return color


def render_message(
        request: Request,
        message: str,
        title: str = "Сообщение",
        back_url: str = "/",
        button_text: str = "На главную",
        current_user: dict | None = None,
):
    """Вспомогательный генератор страницы с определенным сообщением"""
    context = {
        "request": request,
        "title": title,
        "message": message,
        "back_url": back_url,
        "button_text": button_text,
        "user": current_user
    }
    return templates.TemplateResponse(
        "message.html",
        context
    )


async def get_current_user(
        request: Request,
        client_service: IClientService = Depends(get_client_service)
) -> dto.UserProfileDTO | None:
    """
    Возвращает информацию о текущем пользователе из токена.
    При необходимости обновляет токен.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    user = await client_service.get_current_user(access_token)
    return user
