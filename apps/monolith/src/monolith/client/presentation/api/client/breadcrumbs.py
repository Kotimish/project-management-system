from monolith.client.presentation.api.breadcrumbs import get_base_breadcrumbs
from monolith.client.presentation.schemas.breadcrumb import Breadcrumb


def get_home_breadcrumb() -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для главной страницы"""
    return get_base_breadcrumbs(is_active=True)
