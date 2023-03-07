from typing import Dict, Optional

import jwt
from kink import inject
from starlette.requests import Request

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings
from app_api.modules.user.entitys.user import User
from app_api.modules.user.infrastructure.dtos.auth_dto import AuthDto
from app_api.modules.user.infrastructure.dtos.user_dto import UserDto
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


@inject
class AuthUseCase:
    settings: Settings
    user_repository: UserRepository

    def __init__(self, settings: Settings, user_repository: UserRepository, ):
        self.settings = settings
        self.user_repository = user_repository

    async def __call__(self, request: Request) -> AuthDto:
        data: Dict = await request.json()
        user_dto: UserDto = UserDto.from_json(data=data)
        user_from_request: User = user_dto.to_entity()

        user_from_request.is_valid()

        user: Optional[User]

        user = await self.user_repository.find_by_social(
            provider_type=user_from_request.provider.provider_type,
            uid=user_from_request.provider.uid, )

        if user.register_status is False:
            raise CoreException(message='User is not register', )

        if not user:
            user = user_from_request.copy_with(
                ads=True, paid_subscriber=False,
                chat_user_id_block=None, register_status=True, )

        user: User = await self.user_repository.create_or_update(user=user)

        jwt_encode = jwt.encode(
            payload={
                'user.user_id': user.user_id, },
            key=self.settings.jwt_secret,
            algorithm='HS256')

        return AuthDto(
            token=jwt_encode,
            user=UserDto.from_entity(user=user, ), )
