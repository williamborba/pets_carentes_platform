from pydantic.dataclasses import dataclass

from app_api.core.infrastructure.dataclass_config import DataClassConfig
from app_api.modules.user.entitys.user import User
from app_api.modules.user.infrastructure.dtos.user_dto import UserDto


@dataclass(frozen=True, config=DataClassConfig, )
class AuthDto:
    token: str
    user: UserDto

    def to_json(self):
        return {
            'token': self.token,
            'user': self.user.to_json()
        }

    @classmethod
    def from_entity(cls, user: User, token: str) -> 'AuthDto':
        return AuthDto(
            token=token,
            user=UserDto.from_entity(user=user, ), )
