from sentry_sdk import capture_exception
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_api.core.infrastructure.decorators.auth_decorator import auth_decorator
from app_api.modules.user.application.usecases.auth_usecase import AuthUseCase
from app_api.modules.user.infrastructure.dtos.auth_dto import AuthDto


@auth_decorator(authorization=False, )
async def auth(request: Request):
    auth_use_case: AuthUseCase = AuthUseCase()

    try:
        auth_dto: AuthDto = await auth_use_case.__call__(request=request)

        return JSONResponse(content=auth_dto.to_json(), )

    except Exception as error:
        capture_exception(error)
        return JSONResponse(content=str(error), status_code=400, )
