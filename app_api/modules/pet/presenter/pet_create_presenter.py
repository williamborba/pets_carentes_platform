from sentry_sdk import capture_exception
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.infrastructure.decorators.auth_decorator import auth_decorator
from app_api.modules.pet.application.usecases.pet_create_or_update_usecase import PetCreateOrUpdateUseCase
from app_api.modules.pet.application.usecases.pet_photo_create_usecase import PetPhotoCreateUseCase
from app_api.modules.pet.infrastructure.dtos.pet_dto import PetDto


@auth_decorator(authorization=True, )
async def create_or_update(request: Request) -> JSONResponse:
    try:
        pet_create_or_update_usecase: PetCreateOrUpdateUseCase = PetCreateOrUpdateUseCase(
            user=request.scope.get('auth_user', None), )

        pet_dto: PetDto = await pet_create_or_update_usecase.__call__(
            request=request)

        return JSONResponse(content=pet_dto.to_json(), )

    except CoreException as error:
        capture_exception(error)
        return JSONResponse(content='Not Authorized', status_code=400, )

    except Exception as error:
        capture_exception(error)
        return JSONResponse(content='Error', status_code=500, )


@auth_decorator(authorization=True, )
async def photo_create(request: Request) -> JSONResponse:
    try:
        pet_photo_create_usecase: PetPhotoCreateUseCase = PetPhotoCreateUseCase(
            user=request.scope.get('auth_user', None), )

        pet_dto: PetDto = await pet_photo_create_usecase.__call__(request=request)

        return JSONResponse(content=pet_dto.to_json(with_parent=True, ), )

    except CoreException as error:
        capture_exception(error)
        return JSONResponse(content='Not Authorized', status_code=400, )

    except Exception as error:
        capture_exception(error)
        return JSONResponse(content='Error', status_code=500, )
