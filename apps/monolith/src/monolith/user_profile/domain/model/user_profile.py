from datetime import datetime, date

from monolith.user_profile.domain.exceptions import user_profile_exception as exceptions
from monolith.user_profile.domain.model.mixins import IdMixin, TimestampMixin


class UserProfile(IdMixin, TimestampMixin):
    """Класс модели-сущности профиля пользователя"""

    def __init__(
            self,
            auth_user_id: int,
            display_name: str,
            first_name: str | None = None,
            middle_name: str | None = None,
            last_name: str | None = None,
            description: str | None = None,
            birthdate: date | None = None,
            phone: str | None = None,
            profile_id: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None
    ):
        # Вызов родительских классов-миксинов
        IdMixin.__init__(self, profile_id)
        TimestampMixin.__init__(self, created_at, updated_at)
        # Обязательные атрибуты
        self.auth_user_id = auth_user_id
        self.display_name = display_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.description = description
        self.birthdate = birthdate
        self.phone = phone
        # Валидация
        self._validate()

    def _validate(self):
        if not self.auth_user_id:
            raise exceptions.InvalidExternalIdException("Role name is required")
        if not self.display_name:
            raise exceptions.InvalidDisplayNameException("Role name is required")

    def update_display_name(
            self,
            display_name: str
    ):
        """Обновление отображаемого имени"""
        self.display_name = display_name
        self.touch()

    def update_personal_info(
            self,
            first_name: str | None,
            middle_name: str | None,
            last_name: str | None,
    ):
        """Обновление персональных данных"""
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.touch()

    def update_description(
            self,
            description: str | None,
    ):
        """Обновление БИО профиля"""
        self.description = description
        self.touch()

    def update_contact_info(
            self,
            phone: str | None,
    ):
        """Обновление контактной информации"""
        self.phone = phone
        self.touch()

    def update_secondary_info(
            self,
            birthdate: date | None,
    ):
        """Обновление вторичной информации"""
        self.birthdate = birthdate
        self.touch()
