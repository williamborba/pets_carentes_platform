import datetime
import json
from typing import Dict

import pytest
from kink import di
from starlette.requests import Request, Message

from app_api.core.settings import Settings
from app_api.main import app
from app_api.modules.pet.application.usecases.pet_create_or_update_usecase import PetCreateOrUpdateUseCase
from app_api.modules.pet.entitys.pet import Pet, Location, Coordinates, Accept, Specie, Gender, PetStatus
from app_api.modules.pet.infrastructure.di.pet_di import PetDi
from app_api.modules.pet.infrastructure.dtos.pet_dto import PetDto
from app_api.modules.pet.infrastructure.repositorys.pet_repository import PetRepository


async def mock_body_pet_create_needy_success() -> Message:
    mock: Dict = {
        "location": {
            'type': 'Point',
            'coordinates': {'longitude': 1.0, 'latitude': 1.0, },
        },
        "accept": 1,
        "specie": 1,
        "gender": 2,
        "status": 1,
        "date_birth": "2022-09-07T12:40:16Z",
        "date_create": "2022-12-12T10:53:38Z",
        "date_update": "2022-08-10T19:07:36Z",
        "date_publish": "2023-02-02T18:45:42Z",
        "page_link": "https://cargocollective.com/lacinia/eget/tincidunt/eget/tempus/vel.jsp?pellentesque=tincidunt",
        "photos": [
            {
                'asset': 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png',
                'featured': True,
                'register_status': True,
            }
        ],
        "user_origin_id": "e14f3f44-1d9a-4fb3-8c3a-f9b9cf8d65f9",
        "user_guard_id": None,
        "user_candidate_ids": "6467a2e2-f1ec-42df-ae11-1a47c8003788",
        "health_ids": "4f70036f-5fa7-422e-92d2-b5ba8fef004a",
        "hits": 0,
        "days_left_expired": 0,
        "register_status": True
    }

    return {
        'type': 'http.request',
        'body': json.dumps(mock).encode('utf-8'),
    }


async def mock_body_pet_create_origin_adopt_success() -> Message:
    mock: Dict = {
        "location": {
            'type': 'Point',
            'coordinates': {'longitude': 1.0, 'latitude': 1.0, },
        },
        "accept": 1,
        "specie": 1,
        "gender": 2,
        "status": 3,
        "date_birth": "2022-09-07T12:40:16Z",
        "date_create": "2022-12-12T10:53:38Z",
        "date_update": "2022-08-10T19:07:36Z",
        "date_publish": "2023-02-02T18:45:42Z",
        "page_link": "https://cargocollective.com/lacinia/eget/tincidunt/eget/tempus/vel.jsp?pellentesque=tincidunt",
        "photos": None,
        "user_origin_id": "e14f3f44-1d9a-4fb3-8c3a-f9b9cf8d65f9",
        "user_guard_id": "e14f3f44-1d9a-4fb3-8c3a-f9b9cf8d65f9",
        "user_candidate_ids": None,
        "health_ids": None,
        "hits": 0,
        "days_left_expired": 0,
        "register_status": True
    }

    return {
        'type': 'http.request',
        'body': json.dumps(mock).encode('utf-8'),
    }


@pytest.mark.asyncio
async def test_pet_create_service():
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
        ],
        "client": ("134.56.78.4", 1453),
        "server": ("www.example.org", 443),
    }
    settings: Settings = di[Settings]
    app.build_middleware_stack()
    PetDi()
    pet_repository: PetRepository = di[PetRepository]
    pet_create_usecase: PetCreateOrUpdateUseCase = PetCreateOrUpdateUseCase(settings=settings,
                                                                            pet_repository=pet_repository)
    request_create_needy_success = Request(scope, receive=mock_body_pet_create_needy_success)

    pet_dto: PetDto = await pet_create_usecase.__call__(request=request_create_needy_success)
    assert pet_dto == PetDto.from_entity(
        pet=Pet(
            pet_id=pet_dto.pet_id,
            location=Location(
                type='Point',
                coordinates=Coordinates(
                    longitude=1.0,
                    latitude=1.0, ), ),
            accept=Accept(value=Accept.PENDING),
            specie=Specie(value=Specie.DOG),
            gender=Gender(value=Gender.FEMALE),
            status=PetStatus(value=PetStatus.STATUS_NEEDY),
            date_birth=datetime.datetime.fromisoformat('2022-09-07T12:40:16Z'),
            date_create=pet_dto.date_create,
            date_update=None,
            date_publish=None,
            photos=None,
            page_link="https://cargocollective.com/lacinia/eget/tincidunt/eget/tempus/vel.jsp?pellentesque=tincidunt",
            user_origin_id="e14f3f44-1d9a-4fb3-8c3a-f9b9cf8d65f9",
            user_guard_id=None,
            user_candidate_ids=None,
            health_ids=None,
            hits=0,
            days_left_expired=None,
            register_status=True, ), )

    request_origin_adopt_success = Request(scope, receive=mock_body_pet_create_origin_adopt_success)

    pet_dto: PetDto = await pet_create_usecase.__call__(request=request_origin_adopt_success)
    assert pet_dto == PetDto.from_entity(
        pet=Pet(
            pet_id=pet_dto.pet_id,
            location=Location(
                type='Point',
                coordinates=Coordinates(
                    longitude=1.0,
                    latitude=1.0, ), ),
            accept=Accept(value=Accept.PENDING),
            specie=Specie(value=Specie.DOG),
            gender=Gender(value=Gender.FEMALE),
            status=PetStatus(value=PetStatus.STATUS_ORIGIN_ADOPT),
            date_birth=datetime.datetime.fromisoformat('2022-09-07T12:40:16Z'),
            date_create=pet_dto.date_create,
            date_update=None,
            date_publish=None,
            photos=None,
            page_link="https://cargocollective.com/lacinia/eget/tincidunt/eget/tempus/vel.jsp?pellentesque=tincidunt",
            user_origin_id="e14f3f44-1d9a-4fb3-8c3a-f9b9cf8d65f9",
            user_guard_id="e14f3f44-1d9a-4fb3-8c3a-f9b9cf8d65f9",
            user_candidate_ids=None,
            health_ids=None,
            hits=0,
            days_left_expired=None,
            register_status=True, ), )
