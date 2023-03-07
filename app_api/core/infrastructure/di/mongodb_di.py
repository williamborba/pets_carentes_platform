import motor.motor_asyncio
from kink import di

from app_api.core.infrastructure.services.mongodb_service import MongoService


def mongodb_di() -> None:
    di[motor.motor_asyncio.AsyncIOMotorDatabase] = MongoService().get_mongo_database()
