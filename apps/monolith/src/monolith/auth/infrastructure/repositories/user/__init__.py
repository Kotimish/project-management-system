__al__ = {
    "InMemoryUserRepository",
    "ORMUserRepository"
}

from monolith.auth.infrastructure.repositories.user.in_memory import InMemoryUserRepository
from monolith.auth.infrastructure.repositories.user.orm_repository import ORMUserRepository
