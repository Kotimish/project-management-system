from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from monolith.auth.infrastructure.models import Base
from monolith.auth.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin, ExpiresAtMixin, RevokedAtMixin

if TYPE_CHECKING:
    from monolith.auth.infrastructure.models import User


class Session(IdIntPkMixin, TimestampMixin, ExpiresAtMixin, RevokedAtMixin, Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="sessions",
    )
