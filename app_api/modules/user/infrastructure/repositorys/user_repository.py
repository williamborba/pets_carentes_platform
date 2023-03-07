from datetime import datetime
from typing import Optional, Dict

import motor.motor_asyncio
from bson import ObjectId
from kink import inject
from pymongo.results import InsertOneResult, UpdateResult

from app_api.core.exceptions.core_exception import CoreException
from app_api.modules.user.entitys.user import User, ProviderType
from app_api.modules.user.infrastructure.dtos.user_dto import UserDto


@inject
class UserRepository:
    COLLECTION_USER_NAME: str = 'user'
    mongo_database: motor.motor_asyncio.AsyncIOMotorDatabase
    user_collection: motor.motor_asyncio.AsyncIOMotorCollection

    def __init__(self, mongo_database: motor.motor_asyncio.AsyncIOMotorDatabase, ):
        self.mongo_database = mongo_database
        self.user_collection = mongo_database[self.COLLECTION_USER_NAME]

    async def create_or_update(self, user: User) -> User:
        if user.user_id is not None:
            user_update: UpdateResult = await self.user_collection.update_one(
                filter={'_id': ObjectId(oid=user.user_id, )},
                update={'$set': {
                    'provider.name': user.provider.name,
                    'provider.email': user.provider.email,
                    'provider.photo': user.provider.photo,
                    'fcm_token': user.fcm_token,
                    'platform': user.platform,
                    'date_update': datetime.now().isoformat()}}, )

            if user_update.matched_count != 1 and user_update.modified_count != 1:
                raise CoreException('Error in user update.')

            return await self.find_by_id(user_id=user.user_id, )

        user = user.copy_with(
            date_create=datetime.now())

        user_mongo_insert: InsertOneResult = await self.user_collection.insert_one(
            UserDto.from_entity(user=user).to_json(without_id=True), )

        if user_mongo_insert.inserted_id is None:
            raise CoreException('Error in user create.')

        return await self.find_by_id(user_id=user_mongo_insert.inserted_id)

    async def find_by_id(self, user_id: str, ) -> User:
        user_find: Optional[Dict] = await self.user_collection.find_one(
            filter={
                '_id': ObjectId(oid=user_id, )}, )

        if not user_find:
            raise CoreException(message='find by id error.')

        return UserDto.from_json(data=user_find, object_id=True).to_entity()

    async def find_by_email(self, provider_type: ProviderType, email: str, password: str, ) -> Optional[User]:
        user_find: Optional[Dict] = await self.user_collection.find_one(
            filter={
                'provider.provider_type': provider_type.value,
                'provider.email': email,
                'provider.password': password}, )

        if not user_find:
            return None

        return UserDto.from_json(data=user_find, object_id=True).to_entity()

    async def find_by_social(self, provider_type: ProviderType, uid: int, ) -> Optional[User]:
        user_find: Optional[Dict] = await self.user_collection.find_one(
            filter={
                'provider.provider_type': provider_type.value,
                'provider.uid': uid}, )

        if not user_find:
            return None

        return UserDto.from_json(data=user_find, object_id=True).to_entity()
