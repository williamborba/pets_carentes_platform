import rq
from kink import di

from app_api.core.infrastructure.services.redis_service import RedisService


def redis_di() -> None:
    di[rq.Queue] = RedisService().redis_connection()
