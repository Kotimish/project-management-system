from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


class ExpiresAtMixin:
    expires_at: Mapped[datetime] = mapped_column(
        default=None,
        server_default=None,
        nullable=True,
    )
