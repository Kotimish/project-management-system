from contextlib import asynccontextmanager

from fastapi import FastAPI
from pathlib import Path

from monolith.auth.infrastructure.repositories.role.in_memory import InMemoryRoleRepository
from monolith.auth.infrastructure.repositories.session.in_memory import InMemorySessionRepository
from monolith.auth.infrastructure.repositories.user.in_memory import InMemoryUserRepository

from monolith.config.settings import BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Setup ---
    # TODO: Временное решение
    # Создаем репозитории и загружаем данные
    role_repository = InMemoryRoleRepository(Path(BASE_DIR / "src" / "monolith" / "auth" / "data" / "role.json"))
    user_repository = InMemoryUserRepository(Path(BASE_DIR / "src" / "monolith"/ "auth" / "data" / "user.json"))
    session_repository = InMemorySessionRepository(Path(BASE_DIR / "src" / "monolith" / "auth" / "data" / "session.json"))
    # Сохранение ссылок на репозитории в состоянии приложения
    app.state.role_repository = role_repository
    app.state.user_repository = user_repository
    app.state.session_repository = session_repository
    yield
    # --- Teardown ---
