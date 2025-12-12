from abc import ABC, abstractmethod

from monolith.auth.application.dtos.user import CreateUserCommand
from monolith.auth.domain.model.user import User


class IUserFactory(ABC):
    """Интерфейс фабрики модели Пользователь"""
    @abstractmethod
    def create(self, data: CreateUserCommand, hashed_password: str, role_id: int) -> User:
        raise NotImplementedError
