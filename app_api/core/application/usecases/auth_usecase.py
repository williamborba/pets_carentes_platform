from typing import Dict, Any, Optional

import jwt
from kink import inject
from starlette.authentication import AuthenticationError
from starlette.requests import Request

from app_api.core.settings import Settings
from app_api.modules.user.entitys.user import User
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


@inject
class AuthUseCase:
    settings: Settings
    user_repository: UserRepository

    def __init__(self, settings: Settings, user_repository: UserRepository, ):
        self.settings = settings
        self.user_repository = user_repository

    async def __call__(self, request: Request, authorization: bool, ) -> Optional[User]:
        if 'x-api-key' not in request.headers:
            raise AuthenticationError('Invalid authentication credentials')

        if request.headers['x-api-key'] != self.settings.api_secret:
            raise AuthenticationError('Invalid authentication credentials')

        if not authorization:
            return

        if 'Authorization' not in request.headers:
            raise AuthenticationError('Invalid authentication credentials')

        try:
            scheme, credential = request.headers['Authorization'].split(sep=' ')

            if scheme != 'Bearer':
                raise AuthenticationError('Invalid authentication credentials')

            jwt_decode: Dict[str, Any] = jwt.decode(
                jwt=credential, key=self.settings.jwt_secret, algorithms=['HS256', ], )

            if jwt_decode.get('user.user_id', None) is None:
                raise AuthenticationError('Invalid authentication credentials')

            return await self.user_repository.find_by_id(
                user_id=jwt_decode['user.user_id'])

        except Exception:
            raise AuthenticationError('Invalid authentication credentials')
