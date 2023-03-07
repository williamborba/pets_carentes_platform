import redis
import rq
from kink import inject

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings


@inject
class RedisService:
    settings: Settings

    def __init__(self, settings: Settings, ):
        self.settings = settings

    def redis_connection(self, ) -> rq.Queue:
        try:
            redis_connection = redis.Redis(
                host=self.settings.database_queue_host,
                port=self.settings.database_queue_port,
                password=self.settings.database_queue_password, )

            rq.use_connection(redis_connection)
            redis_queue = rq.Queue(connection=redis_connection)

            return redis_queue

        except CoreException as error:
            raise CoreException(error.message)
