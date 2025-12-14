from abc import ABC, abstractmethod

from monolith.client.application.dtos import user_profile as dto


class IUserProfileService(ABC):
    """Интерфейс сервиса профиля пользователя"""

    @abstractmethod
    async def create_profile(
            self,
            data: dto.CreateUserProfileCommand,
    ) -> dto.CreateUserProfileResponse | None:
        """Создание нового профиля пользователя"""
        raise NotImplementedError

    @abstractmethod
    async def get_profile_by_id(self, profile_id: int) -> dto.GetUserProfileResponse | None:
        """Получение профиля пользователя по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_profile_by_auth_user_id(self, auth_user_id: int) -> dto.GetUserProfileResponse | None:
        """Получение профиля пользователя по внешнему id пользователя из сервиса авторизации"""
        raise NotImplementedError

    @abstractmethod
    async def update_profile(
            self,
            profile_id: int,
            data: dto.UpdateUserProfileCommand,
            access_token: str
    ) -> dto.UpdateUserProfileResponse | None:
        """Обновление профиля пользователя по id"""
        raise NotImplementedError
