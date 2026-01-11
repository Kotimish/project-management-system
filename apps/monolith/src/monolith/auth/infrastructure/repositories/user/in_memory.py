import json
from pathlib import Path

from monolith.auth.domain.interfaces.repositories.user_repository import IUserRepository
from monolith.auth.domain.model.user import User


class InMemoryUserRepository(IUserRepository):
    """Реализация репозитория пользователей в памяти с загрузкой из json"""
    def __init__(self, json_path: Path):
        self._storage: dict[int, User] = {}
        self._count: int = 0
        self.json_path = json_path
        self._load_from_json()

    def _load_from_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            # Преобразование в сущности
            self._storage = {
                idx: User(**item)
                for idx, item in enumerate(raw_data)
            }
            for idx, value in self._storage.items():
                value.id = idx
            self._count = len(self._storage)

    async def add(self, user: User) -> User:
        user.id = self._count
        self._storage[self._count] = user
        self._count += 1
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return self._storage.get(user_id)

    async def get_by_login(self, login: str) -> User | None:
        for user in self._storage.values():
            if user.login == login:
                return user
        return None

    async def get_all(self) -> list[User]:
        return list(self._storage.values())

    async def update(self, user_id: int, user: User) -> User | None:
        # Проверка на существование
        if user_id not in self._storage:
            return None
        # Обновление модели в словаре
        user.id = user_id
        self._storage[user_id] = user
        # Возвращение обновлённой модели
        return user

    async def remove(self, user_id: int) -> bool:
        try:
            self._storage.pop(user_id)
            return True
        except KeyError:
            return False
