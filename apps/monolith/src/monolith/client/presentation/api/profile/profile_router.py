from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from monolith.client.presentation.api.dependencies import get_current_user
from monolith.client.presentation.api.utils import render_message
from monolith.config.settings import BASE_DIR

router = APIRouter(
    tags=["Client profile pages"]
)

templates = Jinja2Templates(
    directory= BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/profile", response_class=HTMLResponse, include_in_schema=False)
async def profile(
        request: Request,
        current_user: dict = Depends(get_current_user)
):
    """Страница профиля пользователя"""
    if current_user is None:
        return render_message(
            request,
            message="Вы не авторизованы в системе.",
            back_url="/login",
            button_text="Перейти на страницу входа"
        )
    context = {
        "request": request,
        "user": current_user,
        "page_title": "Профиль"
    }
    return templates.TemplateResponse(
        "under_construction.html",
        context
    )
