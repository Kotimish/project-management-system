from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from monolith.project.infrastructure.models import Base
from monolith.project.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin


class Project(IdIntPkMixin, TimestampMixin, Base):
    """ORM-модель Проекта"""

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        default='',
        server_default='',
    )
    owner_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, role={self.name!r}, full_name={self.description!r})"

    def __repr__(self):
        return str(self)
