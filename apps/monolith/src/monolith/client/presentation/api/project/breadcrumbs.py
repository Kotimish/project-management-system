from monolith.client.presentation.api.breadcrumbs import get_base_breadcrumbs
from monolith.client.presentation.schemas import views
from monolith.client.presentation.schemas.breadcrumb import Breadcrumb


# --- Навигационные цепочки для страниц проекта ---

def get_projects_breadcrumbs(is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы списка проектов"""
    base = get_base_breadcrumbs(is_active=False)
    base.append(
        Breadcrumb(
            name="Проекты",
            url="/projects",
            is_active=is_active
        )
    )
    return base


def get_project_create_breadcrumbs(is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для создания страницы проекта"""
    base = get_projects_breadcrumbs(False)
    base.append(
        Breadcrumb(
            name="Создание проекта",
            url=f"/projects/create",
            is_active=is_active
        )
    )
    return base


def get_project_detail_breadcrumbs(project: views.ProjectReference, is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы проекта"""
    base = get_projects_breadcrumbs(is_active=False)
    base.append(
        Breadcrumb(
            name=project.name,
            url=f"/projects/{project.id}",
            is_active=is_active
        )
    )
    return base


def get_project_edit_breadcrumbs(project: views.ProjectReference, is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для редактирования страницы проекта"""
    base = get_project_detail_breadcrumbs(project, False)
    base.append(
        Breadcrumb(
            name="Редактирование проекта",
            url=f"/projects/{project.id,}/edit",
            is_active=is_active
        )
    )
    return base


# --- Навигационные цепочки для страниц спринтов ---

def get_sprints_breadcrumbs(
        project: views.ProjectReference,
        is_active: bool = True
) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы списка спринтов проекта"""
    base = get_project_detail_breadcrumbs(project, False)
    base.append(
        Breadcrumb(
            name="Спринты",
            url=f"/projects/{project.id}/sprints/",
            is_active=is_active
        )
    )
    return base


def get_sprint_create_breadcrumbs(
        project: views.ProjectReference,
        is_active: bool = True
) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы создания спринта проекта"""
    base = get_project_detail_breadcrumbs(project, False)
    base.append(
        Breadcrumb(
            name="Создание спринта",
            url=f"/projects/{project.id}/sprints/create",
            is_active=is_active
        )
    )
    return base


def get_sprint_detail_breadcrumbs(
        project: views.ProjectReference,
        sprint: views.SprintReference,
        is_active: bool = True
) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы спринта проекта"""
    base = get_project_detail_breadcrumbs(project, False)
    base.append(
        Breadcrumb(
            name=sprint.name,
            url=f"/projects/{project.id}/sprints/{sprint.id}",
            is_active=is_active
        )
    )
    return base


def get_sprint_update_breadcrumbs(
        project: views.ProjectReference,
        sprint: views.SprintReference,
        is_active: bool = True
) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы обновления спринта проекта"""
    base = get_sprint_detail_breadcrumbs(project, sprint, False)
    base.append(
        Breadcrumb(
            name="Редактирование спринта",
            url=f"/projects/{project.id}/sprints/{sprint.id}/edit",
            is_active=is_active
        )
    )
    return base

    # --- Навигационные цепочки для страниц задач ---
    return base


def get_task_create_breadcrumbs(
        project: views.ProjectReference,
        sprint: views.SprintReference,
        is_active: bool = True
) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы создания задачи спринта проекта"""
    base = get_sprint_detail_breadcrumbs(project, sprint, False)
    base.append(
        Breadcrumb(
            name="Создание задачи",
            url=f"/projects/{project.id}/sprints/{sprint.id}/tasks/create",
            is_active=is_active
        )
    )
    return base


def get_task_detail_breadcrumbs(
        project: views.ProjectReference,
        sprint: views.SprintReference,
        task: views.TaskReference,
        is_active: bool = True
) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы задачи спринта проекта"""
    base = get_sprint_detail_breadcrumbs(project, sprint, False)
    base.append(
        Breadcrumb(
            name=task.title,
            url=f"/projects/{project.id}/sprints/{sprint.id}/tasks/{task.id}",
            is_active=is_active
        )
    )
    return base


def get_tasks_by_user_breadcrumbs(is_active: bool = True) -> list[Breadcrumb]:
    """Возвращает Навигационную цепочку для страницы списка задач пользователя"""
    base = get_base_breadcrumbs(is_active=False)
    base.append(
        Breadcrumb(
            name="Задачи",
            url="/tasks/by_auth_user_id/{user.auth_user_id}",
            is_active=is_active
        )
    )
    return base
