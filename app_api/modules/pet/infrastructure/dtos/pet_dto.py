from datetime import datetime
from typing import List, Dict, Optional

from bson import ObjectId
from pydantic.dataclasses import dataclass
from starlette.datastructures import UploadFile

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.infrastructure.dataclass_config import DataClassConfig
from app_api.modules.pet.entitys.pet import Pet, Accept, Specie, Gender, PetStatus, Location, Coordinates, Photo
from app_api.modules.user.entitys.user import User
from app_api.modules.user.infrastructure.dtos.user_dto import UserDto
from app_api.modules.user.infrastructure.repositorys.user_repository import UserRepository


@dataclass(frozen=True, config=DataClassConfig, )
class TimelineDto:
    species: List[Specie]
    longitude: float
    latitude: float
    order_date_publish: bool
    meter: int
    offset: int
    limit: int

    @staticmethod
    def from_query_params(data: Dict) -> 'TimelineDto':
        param_specie: Optional[str] = data.get('specie', None)

        if param_specie is None:
            raise CoreException('specie is required')

        param_specie: List[str] = param_specie.split(',')

        return TimelineDto(
            species=[Specie(value=int(specie)) for specie in param_specie],
            longitude=float(data.get('longitude', None)),
            latitude=float(data.get('latitude', None)),
            order_date_publish=data.get('order_date_publish', None),
            meter=int(data.get('meter', None)),
            offset=int(data.get('offset', None)),
            limit=int(data.get('limit', None)), )

    def is_valid(self) -> bool:
        if self.offset < 0:
            raise CoreException('offset is not supported')

        if self.limit < 0:
            raise CoreException('limit is not supported')

        if self.limit > 10:
            raise CoreException('limit is not supported')

        return True


@dataclass(frozen=True, config=DataClassConfig, )
class PhotoUploadDto:
    pet_id: str
    asset: Optional[UploadFile]
    featured: bool

    @staticmethod
    def from_query_params(data: Dict) -> 'PhotoUploadDto':
        featured: Optional[bool] = data.get('featured', None)

        if isinstance(featured, str):
            featured = featured == 'true'

        if featured is False or featured is None:
            featured = False

        return PhotoUploadDto(
            pet_id=data.get('pet_id', None),
            asset=data.get('asset', None),
            featured=featured, )

    def is_valid(self) -> bool:
        if self.asset.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/webp', ]:
            raise CoreException('file type is not supported')

        if self.asset.size > 1024 * 1024 * 3:
            raise CoreException('file size is too large')

        return True


@dataclass(frozen=True, config=DataClassConfig, )
class PhotoDto:
    asset: str
    featured: bool

    @staticmethod
    def from_json(data: Dict) -> 'PhotoDto':
        return PhotoDto(
            asset=data.get('asset', None),
            featured=data.get('featured', None), )

    def to_json(self) -> Dict:
        return {
            'asset': self.asset,
            'featured': self.featured,
        }

    def to_entity(self) -> Photo:
        return Photo(
            asset=self.asset,
            featured=self.featured, )


@dataclass(frozen=True, config=DataClassConfig, )
class CoordinatesDto:
    longitude: float
    latitude: float

    @staticmethod
    def from_json(data: Dict) -> 'CoordinatesDto':
        return CoordinatesDto(
            longitude=data.get('longitude', None),
            latitude=data.get('latitude', None), )

    @staticmethod
    def from_entity(coordinates: Coordinates) -> 'CoordinatesDto':
        return CoordinatesDto(
            longitude=coordinates.longitude,
            latitude=coordinates.latitude, )

    def to_json(self) -> Dict:
        return {
            'longitude': self.longitude,
            'latitude': self.latitude,
        }

    def to_entity(self) -> Coordinates:
        return Coordinates(
            longitude=self.longitude,
            latitude=self.latitude, )


@dataclass(frozen=True, config=DataClassConfig, )
class LocationDto:
    type: str
    coordinates: CoordinatesDto

    @staticmethod
    def from_json(data: Dict) -> 'LocationDto':
        return LocationDto(
            type=data.get('type', None),
            coordinates=CoordinatesDto.from_json(data=data.get('coordinates', None), ), )

    @staticmethod
    def from_entity(location: Location) -> 'LocationDto':
        return LocationDto(
            type=location.type,
            coordinates=CoordinatesDto.from_entity(coordinates=location.coordinates, ), )

    def to_json(self) -> Dict:
        return {
            'type': self.type,
            'coordinates': self.coordinates.to_json(),
        }

    def to_entity(self) -> Location:
        return Location(
            type=self.type,
            coordinates=self.coordinates.to_entity(), )


@dataclass(frozen=True, config=DataClassConfig, )
class PetDto:
    location: LocationDto
    specie: Specie
    gender: Gender
    content: str
    date_birth: datetime
    status: PetStatus
    user_origin_id: UserDto
    date_create: Optional[datetime] = None
    page_link: Optional[int] = None
    hits: Optional[int] = None
    register_status: Optional[bool] = None
    days_left_expired: Optional[int] = None
    accept: Optional[Accept] = None
    pet_id: Optional[str] = None
    date_update: Optional[datetime] = None
    date_publish: Optional[datetime] = None
    photos: Optional[List[PhotoDto]] = None
    user_guard_id: Optional[UserDto] = None
    user_candidate_ids: Optional[List[str]] = None
    health_ids: Optional[List[int]] = None

    @staticmethod
    async def from_json(data: Dict, user_repository: UserRepository, object_id: bool = False) -> 'PetDto':
        date_create: Optional[datetime] = None
        date_update: Optional[datetime] = None
        date_birth: Optional[datetime] = None
        date_publish: Optional[datetime] = None

        if data.get('date_create', None) is not None:
            date_create = datetime.fromisoformat(data.get('date_create'), )

        if data.get('date_update', None) is not None:
            date_update = datetime.fromisoformat(data.get('date_update'))

        if data.get('date_birth', None) is not None:
            date_birth = datetime.fromisoformat(data.get('date_birth'))

        if data.get('date_publish', None) is not None:
            date_publish = datetime.fromisoformat(data.get('date_publish'))

        user_origin_id: User = await user_repository.find_by_id(
            user_id=data.get('user_origin_id', None), )

        user_guard_id: Optional[User] = None

        if data.get('user_guard_id', None) is not None:
            user_guard_id = await user_repository.find_by_id(
                user_id=data.get('user_guard_id', None), )

        return PetDto(
            pet_id=data.get('_id', None) if object_id is False else str(ObjectId(data.get('_id', ''))),
            location=LocationDto.from_json(data=data.get('location', None), ),
            accept=Accept(value=data.get('accept')) if data.get('accept', None) is not None else None,
            specie=Specie(value=data.get('specie')),
            gender=Gender(value=data.get('gender')),
            content=data.get('content', None),
            date_birth=date_birth,
            date_create=date_create,
            date_update=date_update,
            date_publish=date_publish,
            page_link=data.get('page_link', None),
            photos=[PhotoDto.from_json(data=photo) for photo in data.get('photos', [])]
            if data.get('photos', None) is not None else None,
            status=PetStatus(value=data.get('status')),
            user_origin_id=UserDto.from_entity(user=user_origin_id, ),
            user_guard_id=UserDto.from_entity(user=user_guard_id, ) if user_guard_id is not None else None,
            user_candidate_ids=data.get('user_candidate_ids', None),
            health_ids=data.get('health_ids', None),
            hits=data.get('hits', None),
            days_left_expired=data.get('days_left_expired', None),
            register_status=data.get('register_status', None), )

    @staticmethod
    def from_entity(pet: Pet) -> 'PetDto':
        return PetDto(
            pet_id=pet.pet_id,
            location=LocationDto.from_entity(location=pet.location),
            accept=pet.accept,
            specie=pet.specie,
            gender=pet.gender,
            content=pet.content,
            date_birth=pet.date_birth,
            date_create=pet.date_create,
            date_update=pet.date_update,
            date_publish=pet.date_publish,
            page_link=pet.page_link,
            photos=[PhotoDto(asset=photo.asset, featured=photo.featured, ) for
                    photo in pet.photos] if pet.photos is not None else None,
            status=pet.status,
            user_origin_id=UserDto.from_entity(user=pet.user_origin_id),
            user_guard_id=UserDto.from_entity(user=pet.user_guard_id) if pet.user_guard_id is not None else None,
            user_candidate_ids=pet.user_candidate_ids,
            health_ids=pet.health_ids,
            hits=pet.hits,
            days_left_expired=pet.days_left_expired,
            register_status=pet.register_status, )

    def to_json(self, without_id: bool = False, with_parent: bool = False) -> Dict:
        user_guard_id = None

        if self.user_guard_id is not None:
            user_guard_id = self.user_guard_id.user_id

            if with_parent is True:
                user_guard_id = self.user_guard_id.to_json()

        _data: Dict = {
            '_id': self.pet_id,
            'location': self.location.to_json(),
            'accept': self.accept.value,
            'specie': self.specie.value,
            'gender': self.gender.value,
            'content': self.content,
            'date_birth': self.date_birth.isoformat(),
            'date_create': self.date_create.isoformat(),
            'date_update': self.date_update.isoformat() if self.date_update is not None else None,
            'date_publish': self.date_publish.isoformat() if self.date_publish is not None else None,
            'page_link': self.page_link,
            'photos': [photo.to_json() for photo in self.photos] if self.photos is not None else None,
            'status': self.status.value,
            'user_origin_id': self.user_origin_id.user_id if with_parent is False else self.user_origin_id.to_json(),
            'user_guard_id': user_guard_id,
            'user_candidate_ids': self.user_candidate_ids,
            'health_ids': self.health_ids,
            'hits': self.hits,
            'days_left_expired': self.days_left_expired,
            'register_status': self.register_status
        }

        if without_id:
            _data.pop('_id', None)

        return _data

    def to_entity(self) -> Pet:
        return Pet(
            pet_id=self.pet_id,
            location=self.location.to_entity(),
            accept=self.accept,
            specie=self.specie,
            gender=self.gender,
            content=self.content,
            date_birth=self.date_birth,
            date_create=self.date_create,
            date_update=self.date_update,
            date_publish=self.date_publish,
            page_link=self.page_link,
            photos=[photo.to_entity() for photo in self.photos] if self.photos is not None else None,
            status=self.status,
            user_origin_id=self.user_origin_id.to_entity(),
            user_guard_id=self.user_guard_id.to_entity() if self.user_guard_id is not None else None,
            user_candidate_ids=self.user_candidate_ids,
            health_ids=self.health_ids,
            hits=self.hits,
            days_left_expired=self.days_left_expired,
            register_status=self.register_status, )
