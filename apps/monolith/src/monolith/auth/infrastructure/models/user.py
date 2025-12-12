from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from monolith.auth.infrastructure.models import Base
from monolith.auth.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin, RevokedAtMixin

if TYPE_CHECKING:
    from monolith.auth.infrastructure.models import Role, Session


class User(IdIntPkMixin, TimestampMixin, RevokedAtMixin, Base):
    login: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )
    role: Mapped["Role"] = relationship(
        back_populates="users",
    )
    sessions: Mapped["Session"] = relationship(
        back_populates="user",
    )
