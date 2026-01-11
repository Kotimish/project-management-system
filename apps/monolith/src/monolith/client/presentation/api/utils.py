from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from monolith.client.presentation.api.constants import STATUS_COLOR_MAP, DEFAULT_COLOR
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
