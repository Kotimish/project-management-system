from datetime import date

from pydantic import BaseModel


class GetUserProfileResponse(BaseModel):
    """Данные для ответа на запрос получения профиля пользователя"""
    auth_user_id: int
    display_name: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    description: str | None
    birthdate: date | None
    phone: str | None


class UpdateUserProfileRequest(BaseModel):
    """Данные для запроса обновления профиля пользователя"""
    display_name: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    description: str | None
    birthdate: date | None
    phone: str | None
