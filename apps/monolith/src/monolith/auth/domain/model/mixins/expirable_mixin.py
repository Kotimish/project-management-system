from datetime import datetime, timezone


class ExpirableMixin:
    def __init__(self, created_at: datetime | None = None):
        self.expires_at = created_at
