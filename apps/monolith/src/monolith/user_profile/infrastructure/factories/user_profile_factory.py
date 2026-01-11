from monolith.user_profile.application.dtos.user_profile import CreateUserProfileCommand
from monolith.user_profile.application.interfaces.factories import IUserProfileFactory
from monolith.user_profile.domain.model import UserProfile


class UserProfileFactory(IUserProfileFactory):
    """Реализация фабрики модели профиля пользователя"""
    def create(self, data: CreateUserProfileCommand) -> UserProfile:
        return UserProfile(
            auth_user_id=data.auth_user_id,
            display_name=data.display_name
        )
