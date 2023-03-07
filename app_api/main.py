import logging

from starlette.applications import Starlette

from app_api.core.infrastructure.services.sentry_service import SentryService
from app_api.dependency_injection import di_init
from app_api.modules.pet.presenter.routes import routes as pet_routes
from app_api.modules.user.presenter.routes import routes as user_routes

# logging config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
    handlers=[logging.StreamHandler()])
# dependency injection config
di_init()
# sentry config
SentryService()
# starlette config
app = Starlette(
    debug=True,
    routes=[*user_routes, *pet_routes], )
