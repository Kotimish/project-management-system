from pydantic import BaseModel


class UpdateProjectCommand(BaseModel):
    """Данные для запроса обновления проекта"""
    name: str | None
    description: str | None