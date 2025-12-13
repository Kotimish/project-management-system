from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from monolith.client.presentation.api.dependencies import get_current_user
from monolith.config.settings import BASE_DIR

router = APIRouter(
    tags=["Client main pages"]
)

templates = Jinja2Templates(
    directory= BASE_DIR / "src" / "monolith" / "client" / "presentation" / "templates"
)


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(
        request: Request,
        current_user: dict = Depends(get_current_user)
):
    """Главная страница сайта"""
    context = {
        "request": request,
        "user": current_user
    }
    return templates.TemplateResponse(
        "index.html",
        context
    )


@router.get("/about", response_class=HTMLResponse, include_in_schema=False)
async def about(
        request: Request,
        current_user: dict = Depends(get_current_user)
):
    """Страница о программе"""
    context = {
        "request": request,
        "user": current_user,
        "page_title": "О нас"
    }
    return templates.TemplateResponse(
        "under_construction.html",
        context
    )
