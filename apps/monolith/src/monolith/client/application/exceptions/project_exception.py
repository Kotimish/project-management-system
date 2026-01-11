from monolith.client.application.exceptions.base_exception import BaseClientException


class ProjectException(BaseClientException):
    """Базовое исключение для модели проект"""


class ProjectNotFoundError(ProjectException):
    """Исключение для несуществующего проекта"""


class ProjectForbiddenError(ProjectException):
    """Исключение при попытке получения доступа к проекту без соответствующих прав"""


class ProjectCannotBeDeletedException(ProjectException):
    """Исключение при невозможности удалить проект из-за связанных сущностей"""
