from datetime import datetime, timezone


class RevokedAtMixin:
    def __init__(self, revoked_at: datetime | None = None):
        self.revoked_at = revoked_at
