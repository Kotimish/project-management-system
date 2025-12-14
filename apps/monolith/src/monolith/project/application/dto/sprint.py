from datetime import date

from pydantic import BaseModel


class UpdateSprintCommand(BaseModel):
    """Данные для запроса обновления спринта"""
    name: str | None
    start_date: date | None
    end_date: date | None
