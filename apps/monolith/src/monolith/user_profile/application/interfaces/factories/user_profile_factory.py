from abc import ABC, abstractmethod

from monolith.user_profile.application.dtos.user_profile import CreateUserProfileCommand
from monolith.user_profile.domain.model import UserProfile


class IUserProfileFactory(ABC):
    """Интерфейс фабрики модели профиля пользователя"""
    @abstractmethod
    def create(self, data: CreateUserProfileCommand) -> UserProfile:
        raise NotImplementedError
