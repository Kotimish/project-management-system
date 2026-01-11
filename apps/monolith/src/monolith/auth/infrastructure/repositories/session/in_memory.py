import json
from pathlib import Path

from monolith.auth.domain.interfaces.repositories.session_repository import ISessionRepository
from monolith.auth.domain.model.session import Session


class InMemorySessionRepository(ISessionRepository):
    """Реализация репозитория для сессий пользователей в памяти с загрузкой из json"""
    def __init__(self, json_path: Path):
        self._storage: dict[int, Session] = {}
        self._count: int = 0
        self.json_path = json_path
        self._load_from_json()

    def _load_from_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            # Преобразование в сущности
            self._storage = {
                idx: Session(**item)
                for idx, item in enumerate(raw_data)
            }
            for idx, value in self._storage.items():
                value.id = idx
            self._count = len(self._storage)

    async def add(self, session: Session) -> Session:
        session.id = self._count
        self._storage[self._count] = session
        self._count += 1
        return session

    async def get_by_id(self, session_id: int) -> Session | None:
        return self._storage.get(session_id)

    async def get_all(self) -> list[Session]:
        return list(self._storage.values())

    async def update(self, session_id: int, session: Session) -> Session | None:
        # Проверка на существование
        if session_id not in self._storage:
            return None
        # Обновление модели в словаре
        session.id = session_id
        self._storage[session_id] = session
        # Возвращение обновлённой модели
        return session

    async def remove(self, session_id: int) -> bool:
        try:
            self._storage.pop(session_id)
            return True
        except KeyError:
            return False
