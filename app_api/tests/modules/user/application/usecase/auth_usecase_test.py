import json
from typing import Dict

import pytest
from kink import di
from starlette.requests import Request, Message

from app_api.core.settings import Settings
from app_api.main import app
from app_api.modules.user.application.usecases.auth_usecase import AuthUseCase
from app_api.modules.user.entitys.user import User, Provider, Profile, ProviderType, ProfileType
from app_api.modules.user.infrastructure.di.user_di import UserDi
from app_api.modules.user.infrastructure.dtos.auth_dto import AuthDto
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


async def mock_body_auth_success() -> Message:
    mock: Dict = {
        "provider": {
            "provider_type": 1,
            "uid": 1234567890,
            "email": "wborba.dev@gmail.com",
            "password": None,
            "photo": None,
            "name": "William Borba"
        },
        "profile": {
            "profile_type": 2,
            "name": None,
            "photo": None,
            "whatsapp": None,
            "instagram": None,
            "facebook": None,
            "donation": None
        },
        "fcm_token": "token123",
        "platform": "android",
        "ads": True,
        "paid_subscriber": False,
        "chat_user_id_block": None,
        "register_status": True
    }

    return {
        'type': 'http.request',
        'body': json.dumps(mock).encode('utf-8'),
    }


@pytest.mark.asyncio
async def test_auth_service():
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "https",
        "path": "/",
        "query_string": b"a=123&b=456",
        "headers": [
            (b"host", b"www.example.org"),
            (b"content-type", b"application/json"),
            (b"content-length", b"18"),
            (b"accept", b"application/json"),
            (b"accept", b"text/plain"),
            (b"x-api-key", b"$_><|[?:_=|=/=[$!`&^\.^^*@!=(^-}!+=;*-*~"),
        ],
        "client": ("134.56.78.4", 1453),
        "server": ("www.example.org", 443),
    }
    settings: Settings = di[Settings]
    app.build_middleware_stack()
    UserDi()
    user_repository: UserRepository = di[UserRepository]
    auth_usecase: AuthUseCase = AuthUseCase(settings=settings, user_repository=user_repository, )
    request_auth_success = Request(scope, receive=mock_body_auth_success)

    auth_dto: AuthDto = await auth_usecase.__call__(request=request_auth_success)
    assert auth_dto == AuthDto.from_entity(
        token=auth_dto.token,
        user=User(
            user_id=auth_dto.user.user_id,
            provider=Provider(
                provider_type=ProviderType(value=ProviderType.GOOGLE),
                uid=1234567890, email='wborba.dev@gmail.com',
                name='William Borba', password=None, photo=None, ),
            profile=Profile(
                profile_type=ProfileType(value=ProfileType.COMMON),
                name=None, photo=None, whatsapp=None,
                instagram=None, facebook=None, donation=None, ),
            fcm_token='token123',
            platform='android',
            date_create=auth_dto.user.date_create,
            date_update=auth_dto.user.date_update,
            ads=True,
            paid_subscriber=False,
            chat_user_id_block=None,
            register_status=True, ), )
