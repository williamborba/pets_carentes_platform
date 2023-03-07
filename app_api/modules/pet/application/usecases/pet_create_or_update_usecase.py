from datetime import datetime
from typing import Dict, Optional

from kink import inject
from starlette.requests import Request

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings
from app_api.modules.pet.entitys.pet import Pet, Accept
from app_api.modules.pet.infrastructure.dtos.pet_dto import PetDto
from app_api.modules.pet.infrastructure.repositorys.pet_repository import PetRepository
from app_api.modules.user.entitys.user import User
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


@inject
class PetCreateOrUpdateUseCase:
    settings: Settings
    user_repository: UserRepository
    pet_repository: PetRepository
    user: User

    def __init__(self, settings: Settings, user_repository: UserRepository, pet_repository: PetRepository,
                 user: User, ):
        self.settings = settings
        self.user_repository = user_repository
        self.pet_repository = pet_repository
        self.user = user

    async def __call__(self, request: Request) -> PetDto:
        if not self.user.is_active():
            raise CoreException(message='User not active', )

        request_data: Dict = await request.json()

        pet_dto: PetDto = await PetDto.from_json(
            data=request_data, user_repository=self.user_repository, )
        pet: Pet = pet_dto.to_entity()

        if request.method == 'PATCH' and not pet.pet_id:
            raise CoreException(message='Pet id is required', )

        pet_current: Optional[Pet] = None

        if pet.pet_id is not None:
            pet_current: Pet = await self.pet_repository.find_by_id(
                pet_id=pet.pet_id, )

            pet_current.is_valid_for_update(
                user=self.user, pet_new=pet, )

        else:
            pet.is_valid_for_create(
                user=self.user, )

        pet_create_or_update: Pet = await self.pet_repository.create_or_update(
            pet=pet.copy_with(
                pet_id=pet.pet_id,
                accept=Accept(value=Accept.PENDING) if pet.pet_id is None else pet_current.accept,
                date_create=None if pet.pet_id is None else pet_current.date_create,
                date_update=None if pet.pet_id is None else datetime.now(),
                date_publish=None if pet.pet_id is None else pet.date_publish,
                user_candidate_ids=None if pet.pet_id is None else pet.user_candidate_ids,
                health_ids=None if pet.pet_id is None else pet.health_ids,
                hits=0 if pet.pet_id is None else pet.hits,
                days_left_expired=None if pet.pet_id is None else pet.days_left_expired,
                register_status=True, ), )

        return PetDto.from_entity(pet=pet_create_or_update, )
