from starlette.routing import Route

from app_api.modules.user.presenter.auth_presenter import auth

routes = [
    Route(path='/auth', endpoint=auth, methods=['POST'], ),
]
