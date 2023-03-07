from typing import List

from kink import inject
from starlette.requests import Request

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings
from app_api.modules.pet.entitys.pet import Pet
from app_api.modules.pet.infrastructure.dtos.pet_dto import PetDto, TimelineDto
from app_api.modules.pet.infrastructure.repositorys.pet_repository import PetRepository
from app_api.modules.user.entitys.user import User


@inject
class PetTimelineUseCase:
    settings: Settings
    pet_repository: PetRepository
    user: User

    def __init__(self, settings: Settings, pet_repository: PetRepository,
                 user: User, ):
        self.settings = settings
        self.pet_repository = pet_repository
        self.user = user

    async def __call__(self, request: Request) -> List[PetDto]:
        if self.user.register_status is False:
            raise CoreException(message='User not registered', )

        timeline_dto: TimelineDto = TimelineDto.from_query_params(
            data=dict(request.query_params), )

        timeline_dto.is_valid()

        pet_timeline: List[Pet] = await self.pet_repository.timeline(
            species=timeline_dto.species,
            longitude=timeline_dto.longitude, latitude=timeline_dto.latitude,
            order_date_publish=timeline_dto.order_date_publish,
            meter=timeline_dto.meter,
            offset=timeline_dto.offset, limit=timeline_dto.limit, )

        if len(pet_timeline) <= 0:
            return []

        return [PetDto.from_entity(pet=pet, ) for pet in pet_timeline]
