import json
from pathlib import Path

from monolith.auth.domain.interfaces.repositories.role_repository import IRoleRepository
from monolith.auth.domain.model.role import Role


class InMemoryRoleRepository(IRoleRepository):
    """Реализация репозитория ролей пользователей в памяти с загрузкой из json"""
    def __init__(self, json_path: Path):
        self._storage: dict[int, Role] = {}
        self._count: int = 0
        self.json_path = json_path
        self._load_from_json()

    def _load_from_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            # Преобразование в сущности
            self._storage = {
                idx: Role(**item)
                for idx, item in enumerate(raw_data)
            }
            for idx, value in self._storage.items():
                value.id = idx
            self._count = len(self._storage)

    async def add(self, role: Role) -> Role:
        role.id = self._count
        self._storage[self._count] = role
        self._count += 1
        return role

    async def get_by_id(self, role_id: int) -> Role | None:
        return self._storage.get(role_id)

    async def get_by_slug(self, slug: str) -> Role | None:
        for role in self._storage.values():
            if role.slug == slug:
                return role
        return None

    async def get_all(self) -> list[Role]:
        return list(self._storage.values())

    async def update(self, role_id: int, role: Role) -> Role | None:
        # Проверка на существование
        if role_id not in self._storage:
            return None
        # Обновление модели в словаре
        role.id = role_id
        self._storage[role_id] = role
        # Возвращение обновлённой модели
        return role

    async def remove(self, role_id: int) -> bool:
        try:
            self._storage.pop(role_id)
            return True
        except KeyError:
            return False
