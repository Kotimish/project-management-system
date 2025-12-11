from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from monolith.auth.infrastructure.models import Base
from monolith.auth.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin


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

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, role={self.name!r}, slug={self.slug!r}, full_name={self.description!r})"

    def __repr__(self):
        return str(self)
