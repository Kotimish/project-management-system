from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from monolith.client.presentation.api.dependencies import get_current_user
from monolith.client.application.dtos import user_profile as dto
from monolith.client.presentation.schemas import user_profile as schemas
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
        current_user: dto.GetUserProfileResponse = Depends(get_current_user)
):
    """Главная страница сайта"""
    user = None
    if current_user is not None:
        schema = schemas.GetUserProfileResponse(**current_user.model_dump())
        user = schema.model_dump()
    context = {
        "request": request,
        "user": user
    }
    return templates.TemplateResponse(
        "index.html",
        context
    )


@router.get("/about", response_class=HTMLResponse, include_in_schema=False)
async def about(
        request: Request,
        current_user: dto.GetUserProfileResponse = Depends(get_current_user)
):
    """Страница о программе"""
    user = None
    if current_user is not None:
        schema = schemas.GetUserProfileResponse(**current_user.model_dump())
        user = schema.model_dump()
    context = {
        "request": request,
        "user": user,
        "page_title": "О нас"
    }
    return templates.TemplateResponse(
        "under_construction.html",
        context
    )
