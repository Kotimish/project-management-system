from monolith.project.domain.exceptions.base_exception import BaseProjectException


class ProjectException(BaseProjectException):
    """Базовое исключение для доменной модели Проект"""


class InvalidProjectNameException(ProjectException):
    """Исключение для некорректного или отсутствующего названия проекта"""


class InvalidProjectOwnerIdException(ProjectException):
    """Исключение для некорректного или отсутствующего id владельца проекта"""


class ProjectNotFoundError(ProjectException):
    """Исключение для несуществующего Проекта"""


class ProjectCannotBeDeletedException(ProjectException):
    """Исключение при невозможности удалить проект из-за связанных сущностей"""