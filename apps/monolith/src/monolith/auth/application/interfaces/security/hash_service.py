from abc import ABC, abstractmethod


class IHashService(ABC):
    """Интерфейс хеширования чувствительных данных (к примеру, паролей)"""
    @abstractmethod
    def hash(self, data: str) -> str:
        """Хеширование данных"""
        raise NotImplementedError

    @abstractmethod
    def verify(self, data: str, hashed: str) -> bool:
        """Проверка соответствия данных и хеша"""
        raise NotImplementedError
