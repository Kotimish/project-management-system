from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from monolith.project.infrastructure.models import Base
from monolith.project.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin

if TYPE_CHECKING:
    from monolith.project.infrastructure.models import Project


class Sprint(IdIntPkMixin, TimestampMixin, Base):
    """ORM-модель Спринта"""

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id'),
        nullable=False,
    )
    project: Mapped['Project'] = relationship(
        back_populates='sprints'
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, start_date={self.start_date!r}, end_date={self.end_date!r})"

    def __repr__(self):
        return str(self)
