from kink import inject
from starlette.datastructures import FormData
from starlette.requests import Request

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.infrastructure.services.s3_upload_photo_service import S3UploadPhotoService
from app_api.core.settings import Settings
from app_api.modules.pet.entitys.pet import Photo, Pet
from app_api.modules.pet.infrastructure.dtos.pet_dto import PhotoUploadDto, PetDto
from app_api.modules.pet.infrastructure.repositorys.pet_repository import PetRepository
from app_api.modules.user.entitys.user import User
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


@inject
class PetPhotoCreateUseCase:
    settings: Settings
    pet_repository: PetRepository
    user_repository: UserRepository
    user: User

    def __init__(self, settings: Settings, user_repository: UserRepository, pet_repository: PetRepository,
                 user: User, ):
        self.settings = settings
        self.user_repository = user_repository
        self.pet_repository = pet_repository
        self.user = user

    async def __call__(self, request: Request) -> PetDto:
        form: FormData = await request.form()

        photo_upload_dto: PhotoUploadDto = PhotoUploadDto.from_query_params(
            data={**dict(request.query_params), **{'asset': form.get('asset', None), }, }, )

        photo_upload_dto.is_valid()

        pet: Pet = await self.pet_repository.find_by_id(
            pet_id=photo_upload_dto.pet_id, )

        if not pet.is_active() and pet.is_expired():
            raise CoreException('pet is not active or expired')

        if pet.is_limit_photos():
            raise CoreException('pet is limit photos')

        pet.is_valid_for_update(
            user=self.user, pet_new=pet.copy_with(accept=None, ), )

        asset_read: bytes = await photo_upload_dto.asset.read()

        s3_upload_photo_usecase = S3UploadPhotoService()
        asset_name: str = await s3_upload_photo_usecase.__call__(
            asset=asset_read, )

        photo: Photo = Photo(
            asset='%s/%s' % (self.settings.aws_s3_url_prefix, asset_name),
            featured=photo_upload_dto.featured)

        pet = pet.copy_with_photos(
            photo=photo, )

        pet = await self.pet_repository.create_or_update(pet=pet, )

        return PetDto.from_entity(pet=pet, )
