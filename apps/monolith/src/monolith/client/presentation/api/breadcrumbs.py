from monolith.client.presentation.schemas.breadcrumb import Breadcrumb


def get_base_breadcrumbs(is_active: bool = False) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку с базовой страницей"""
    base_breadcrumb = Breadcrumb(
        name="Главная",
        url="/",
        is_active=is_active
    )
    return [base_breadcrumb, ]
