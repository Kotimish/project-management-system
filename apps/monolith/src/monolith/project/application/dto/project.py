from pydantic import BaseModel


class UpdateProjectCommand(BaseModel):
    """Данные для запроса обновления проекта"""
    name: str | None
    description: str | None


class ProjectResponse(BaseModel):
    """Данные для ответа на запрос о получение проекта"""
    id: int
    name: str | None
    description: str | None
