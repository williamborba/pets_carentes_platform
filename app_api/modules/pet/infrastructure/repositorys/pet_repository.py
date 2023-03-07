from datetime import datetime
from typing import Dict, Optional, List

import motor.motor_asyncio
from bson.objectid import ObjectId
from kink import inject
from pymongo.results import InsertOneResult, UpdateResult

from app_api.core.exceptions.core_exception import CoreException
from app_api.modules.pet.entitys.pet import Pet, Accept, Specie
from app_api.modules.pet.infrastructure.dtos.pet_dto import PetDto
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


@inject
class PetRepository:
    COLLECTION_PET_NAME: str = 'pet'
    mongo_database: motor.motor_asyncio.AsyncIOMotorDatabase
    pet_collection: motor.motor_asyncio.AsyncIOMotorCollection
    user_repository: UserRepository

    def __init__(self, mongo_database: motor.motor_asyncio.AsyncIOMotorDatabase, user_repository: UserRepository):
        self.mongo_database = mongo_database
        self.pet_collection = mongo_database[self.COLLECTION_PET_NAME]
        self.user_repository = user_repository

    async def create_or_update(self, pet: Pet) -> Pet:
        if pet.pet_id is not None:

            import logging
            logging.warning('###################################################')
            logging.warning(pet)
            logging.warning('---------------------------------------------------')
            logging.warning(pet.copy_with(date_update=datetime.now(), ))
            logging.warning('---------------------------------------------------')
            logging.warning(PetDto.from_entity(pet.copy_with(date_update=datetime.now(), ), ))
            logging.warning('###################################################')

            pet_update: UpdateResult = await self.pet_collection.update_one(
                filter={'_id': ObjectId(oid=pet.pet_id, )},
                update={'$set': PetDto.from_entity(pet.copy_with(date_update=datetime.now(), ), ).to_json(
                    without_id=True), }, )

            if pet_update.matched_count != 1 and pet_update.modified_count != 1:
                raise CoreException('Error in pet update.')

            return await self.find_by_id(pet_id=pet.pet_id, )

        pet_mongo_insert: InsertOneResult = await self.pet_collection.insert_one(
            PetDto.from_entity(pet=pet.copy_with(date_create=datetime.now(), ), ).to_json(without_id=True), )

        if pet_mongo_insert.inserted_id is None:
            raise CoreException('Error in pet create.')

        return await self.find_by_id(pet_id=pet_mongo_insert.inserted_id)

    async def find_by_id(self, pet_id: str, ) -> Pet:
        pet_find: Optional[Dict] = await self.pet_collection.find_one(
            filter={
                '_id': ObjectId(oid=pet_id, )}, )

        if not pet_find:
            raise CoreException(message='find by id error.')

        pet_dto: PetDto = await PetDto.from_json(
            data=pet_find, user_repository=self.user_repository, object_id=True, )

        return pet_dto.to_entity()

    async def timeline(
            self, species: List[Specie], longitude: float, latitude: float,
            order_date_publish: bool, meter: int, offset: int,
            limit: int, ) -> List[Pet]:
        if offset > 0:
            offset = (offset - 1) * limit

        pipeline: List[Dict] = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude, ], },
                    'distanceField': 'distance.calculated',
                    'maxDistance': meter,
                    'spherical': True}, },
            {
                '$match': {
                    'accept': {
                        '$in': [Accept.TRUE.value, Accept.REVISION.value, ], },
                    'register_status': True,
                    'specie': {
                        '$in': [specie.value for specie in species], }, },
            },
        ]

        if order_date_publish:
            pipeline.append({
                '$sort': {'date_publish': -1, }, }, )

        pipeline.append({'$skip': offset, })
        pipeline.append({'$limit': limit, })

        pet_collection: List[Dict] = await self.pet_collection.aggregate(pipeline, ).to_list(
            length=None, )
        pet_list: List[Pet] = []

        for pet_json in pet_collection:
            pet_dto: PetDto = await PetDto.from_json(
                data=pet_json, user_repository=self.user_repository, object_id=True, )
            pet_list.append(pet_dto.to_entity(), )

        return pet_list
