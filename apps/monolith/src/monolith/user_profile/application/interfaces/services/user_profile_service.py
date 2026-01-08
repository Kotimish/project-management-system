from abc import ABC, abstractmethod

from monolith.user_profile.application.dtos import user_profile as dto


class IUserProfileService(ABC):
    """Интерфейс сервиса работы с профилем пользователей"""

    @abstractmethod
    async def create_profile(self, data: dto.CreateUserProfileCommand) -> dto.CreateUserProfileResponse:
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
    async def get_profiles_by_auth_user_ids(self, auth_user_ids: list[int]) -> list[dto.GetUserProfileResponse]:
        """Получение профилей пользователей по внешним id пользователей из сервиса авторизации"""
        raise NotImplementedError

    @abstractmethod
    async def update_profile(
            self,
            profile_id: int,
            data: dto.UpdateUserProfileCommand
    ) -> dto.UpdateUserProfileResponse | None:
        """Обновление профиля пользователя по id"""
        raise NotImplementedError
