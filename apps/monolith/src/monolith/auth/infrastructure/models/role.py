from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from monolith.auth.infrastructure.models import Base
from monolith.auth.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin

if TYPE_CHECKING:
    from monolith.auth.infrastructure.models import User


class Role(IdIntPkMixin, TimestampMixin, Base):
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        default='',
        server_default='',
    )
    users: Mapped["User"] = relationship(
        back_populates="role",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, role={self.name!r}, slug={self.slug!r}, full_name={self.description!r})"

    def __repr__(self):
        return str(self)
