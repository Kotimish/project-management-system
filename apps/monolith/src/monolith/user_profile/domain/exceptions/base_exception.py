class BaseProfileException(Exception):
    """Базовое исключение для сервиса профилей пользователей"""

    def __init__(self, message: str = '', status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
