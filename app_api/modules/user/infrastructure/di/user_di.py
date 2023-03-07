from kink import di

from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


def user_di() -> None:
    di[UserRepository] = UserRepository()
