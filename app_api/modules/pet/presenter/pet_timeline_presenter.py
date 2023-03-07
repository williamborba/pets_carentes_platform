from typing import List

from sentry_sdk import capture_exception
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.infrastructure.decorators.auth_decorator import auth_decorator
from app_api.modules.pet.application.usecases.pet_timeline_usecase import PetTimelineUseCase
from app_api.modules.pet.infrastructure.dtos.pet_dto import PetDto


@auth_decorator(authorization=True, )
async def timeline(request: Request) -> JSONResponse:
    try:
        pet_timeline_usecase: PetTimelineUseCase = PetTimelineUseCase(
            user=request.scope.get('auth_user', None), )

        pet_dto_timeline: List[PetDto] = await pet_timeline_usecase.__call__(request=request)

        return JSONResponse(
            content=[pet_dto.to_json(with_parent=True, ) for pet_dto in pet_dto_timeline], )

    except CoreException as error:
        capture_exception(error)
        return JSONResponse(content='Not Authorized', status_code=400, )

    except Exception as error:
        capture_exception(error)
        return JSONResponse(content='Error', status_code=500, )
