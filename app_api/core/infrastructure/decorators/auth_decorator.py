import functools
from typing import Optional, Any

import sentry_sdk
from starlette.authentication import AuthenticationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app_api.core.application.usecases.auth_usecase import AuthUseCase
from app_api.modules.user.entitys.user import User


def auth_decorator(authorization: bool = True, ) -> Any:
    def auth_func_decorator(func: Any):
        @functools.wraps(func)
        async def wrapper_auth_decorator(request: Request):
            try:
                auth_usecase = AuthUseCase()
                user: Optional[User] = await auth_usecase.__call__(
                    request=request, authorization=authorization, )

                request.scope['auth_user'] = user

            except AuthenticationError as error:
                sentry_sdk.capture_exception(error)

                return JSONResponse(content='Invalid authentication credentials', status_code=401, )

            return await func(request)

        return wrapper_auth_decorator

    return auth_func_decorator

    # @functools.wraps(func)
    # async def wrapper_auth_decorator(request: Request):
    #     try:
    #         auth_usecase = AuthUseCase()
    #         user: Optional[User] = await auth_usecase.__call__(
    #             request=request, authorization=authorization, )
    #
    #         request.scope['auth_user'] = user
    #
    #     except AuthenticationError as error:
    #         sentry_sdk.capture_exception(error)
    #
    #         return JSONResponse(content='Invalid authentication credentials', status_code=401, )
    #
    #     return await func(request)
    #
    # return wrapper_auth_decorator
