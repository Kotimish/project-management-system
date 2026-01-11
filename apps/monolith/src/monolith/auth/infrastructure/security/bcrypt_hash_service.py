from monolith.auth.application.interfaces.security.hash_service import IHashService
import bcrypt

class BcryptHashService(IHashService):
    """Реализация хеширования чувствительных данных с помощью bcrypt"""
    def hash(self, data: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(data.encode('utf-8'), salt).decode('utf-8')

    def verify(self, data: str, hashed: str) -> bool:
        return bcrypt.checkpw(data.encode('utf-8'), hashed.encode('utf-8'))
