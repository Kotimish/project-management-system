from datetime import date

from pydantic import BaseModel


class UpdateSprintCommand(BaseModel):
    """Данные для запроса обновления спринта"""
    name: str | None
    start_date: date | None
    end_date: date | None


class SprintResponse(BaseModel):
    """Данные для ответа на запрос о получение информации о спринте"""
    id: int
    project_id: int
    name: str | None
    start_date: date
    end_date: date
