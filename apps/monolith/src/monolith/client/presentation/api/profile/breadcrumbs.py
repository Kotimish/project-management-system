from monolith.client.presentation.api.breadcrumbs import get_base_breadcrumbs
from monolith.client.presentation.schemas.breadcrumb import Breadcrumb


def get_profiles_breadcrumbs(is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы списка профилей пользователя"""
    breadcrumbs = get_base_breadcrumbs(is_active=False)
    breadcrumbs.append(
        Breadcrumb(
            name="Профили",
            url=f"/profiles",
            is_active=is_active,
        )
    )
    return breadcrumbs


def get_profile_breadcrumbs(user_id: int, is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы профиля пользователя"""
    breadcrumbs = get_base_breadcrumbs(is_active=False)
    breadcrumbs.append(
        Breadcrumb(
            name="Профиль",
            url=f"/profiles/{user_id}",
            is_active=is_active,
        )
    )
    return breadcrumbs


def get_profile_edit_breadcrumbs(user_id: int) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы редактирования профиля пользователя"""
    breadcrumbs = get_profile_breadcrumbs(user_id, is_active=False)
    breadcrumbs.append(
        Breadcrumb(
            name="Редактирование",
            url=f"/profiles/{user_id}/edit",
            is_active=True,
        )

    )
    return breadcrumbs
