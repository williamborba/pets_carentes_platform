import os

from app_api.core.infrastructure.di.mongodb_di import mongodb_di
from app_api.core.infrastructure.di.redis_di import redis_di
from app_api.core.settings import config_di
from app_api.modules.pet.infrastructure.di.pet_di import pet_di
from app_api.modules.user.infrastructure.di.user_di import user_di


def di_init() -> None:
    config_di(
        path_root=str(os.path.dirname(os.path.abspath(__file__))))
    redis_di()
    mongodb_di()
    user_di()
    pet_di()
