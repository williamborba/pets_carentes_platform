from urllib import parse

import motor.motor_asyncio
from kink import inject

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings, ENV_TEST, ENV_SANDBOX


@inject
class MongoService:
    settings: Settings

    def __init__(self, settings: Settings, ):
        self.settings = settings

    def get_mongo_database(self, ) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        try:
            mongo_client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient((
                f'mongodb://{self.settings.database_primary_username}:'
                f'{parse.quote(self.settings.database_primary_password)}@'
                f'{self.settings.database_primary_host}:27017'))

            if self.settings.env in [ENV_TEST, ENV_SANDBOX, ]:
                mongo_database: motor.motor_asyncio.AsyncIOMotorDatabase = \
                    mongo_client[f'{self.settings.database_primary_name}_test']

            else:
                mongo_database: motor.motor_asyncio.AsyncIOMotorDatabase = \
                    mongo_client[self.settings.database_primary_name]

            return mongo_database

        except CoreException as error:
            raise CoreException(error.message)
