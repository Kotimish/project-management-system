from monolith.client.presentation.api.breadcrumbs import get_base_breadcrumbs
from monolith.client.presentation.schemas.breadcrumb import Breadcrumb


def get_auth_login_breadcrumbs() -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы авторизации пользователя"""
    breadcrumbs = get_base_breadcrumbs(is_active=False)
    breadcrumbs.append(
        Breadcrumb(
            name="Регистрация",
            url="/register",
            is_active=True,
        )
    )
    return breadcrumbs


def get_auth_register_breadcrumbs() -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы регистрации пользователя"""
    breadcrumbs = get_base_breadcrumbs(is_active=False)
    breadcrumbs.append(
        Breadcrumb(
            name="Авторизация",
            url="/login",
            is_active=True,
        )
    )
    return breadcrumbs
