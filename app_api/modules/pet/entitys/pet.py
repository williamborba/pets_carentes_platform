from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic.dataclasses import dataclass

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.infrastructure.dataclass_config import DataClassConfig
from app_api.core.infrastructure.types import EmptyValue
from app_api.modules.user.entitys.user import User


class PetStatus(Enum):
    STATUS_NEEDY: int = 1
    STATUS_ADOPT: int = 2
    STATUS_ORIGIN_ADOPT: int = 3


class Accept(Enum):
    TRUE: int = 1
    PENDING: int = 2
    FALSE: int = 3
    REVISION: int = 4


class Specie(Enum):
    DOG: int = 1
    CAT: int = 2


class Gender(Enum):
    MALE: int = 1
    FEMALE: int = 2


@dataclass(frozen=True, config=DataClassConfig, )
class Photo:
    asset: str
    featured: bool

    def copy_with(self, asset: Optional[str] = EmptyValue, featured: Optional[bool] = EmptyValue, ) -> 'Photo':
        return Photo(
            asset=self.asset if asset is EmptyValue else asset,
            featured=self.featured if featured is EmptyValue else featured, )


@dataclass(frozen=True, config=DataClassConfig, )
class Coordinates:
    longitude: float
    latitude: float


@dataclass(frozen=True, config=DataClassConfig, )
class Location:
    type: str
    coordinates: Coordinates


def is_must_be_empty_for_create(pet: 'Pet', ) -> bool:
    if pet.accept is not None:
        raise CoreException('accept must be None.')

    if pet.date_update is not None:
        raise CoreException('date update must be None.')

    if pet.date_create is not None:
        raise CoreException('date create must be None.')

    if pet.hits is not None:
        raise CoreException('hits must be None.')

    if pet.page_link is not None:
        raise CoreException('page link must be None.')

    if pet.days_left_expired is not None:
        raise CoreException('days left expired must be None.')

    if pet.user_candidate_ids is not None:
        raise CoreException('user candidate ids must be None.')

    if pet.photos is not None:
        raise CoreException('photos must be None.')

    return True


def is_must_be_empty_for_update(pet: 'Pet', ) -> bool:
    if pet.accept is not None:
        raise CoreException('accept must be None.')


@dataclass(frozen=True, config=DataClassConfig, )
class Pet:
    location: Location
    specie: Specie
    gender: Gender
    content: str
    date_birth: datetime
    status: PetStatus
    user_origin_id: User
    date_create: Optional[datetime] = None
    page_link: Optional[int] = None
    hits: Optional[int] = None
    register_status: Optional[bool] = None
    accept: Optional[Accept] = None
    pet_id: Optional[str] = None
    date_update: Optional[datetime] = None
    date_publish: Optional[datetime] = None
    photos: Optional[List[Photo]] = None
    user_guard_id: Optional[User] = None
    user_candidate_ids: Optional[List[str]] = None
    health_ids: Optional[List[int]] = None
    days_left_expired: Optional[int] = None

    def copy_with(self, pet_id: Optional[str] = EmptyValue, location: Optional[Location] = EmptyValue,
                  accept: Optional[Accept] = EmptyValue, content: Optional[str] = EmptyValue,
                  specie: Optional[Specie] = EmptyValue, gender: Optional[Gender] = EmptyValue,
                  date_birth: Optional[datetime] = EmptyValue, date_create: Optional[datetime] = EmptyValue,
                  date_update: Optional[datetime] = EmptyValue, date_publish: Optional[datetime] = EmptyValue,
                  page_link: Optional[str] = EmptyValue, photos: Optional[List[Photo]] = EmptyValue,
                  status: Optional[PetStatus] = EmptyValue, user_origin_id: Optional[User] = EmptyValue,
                  user_guard_id: Optional[User] = EmptyValue, user_candidate_ids: Optional[List[str]] = EmptyValue,
                  health_ids: Optional[List[int]] = EmptyValue, hits: Optional[int] = EmptyValue,
                  days_left_expired: Optional[int] = EmptyValue, register_status: Optional[bool] = EmptyValue) -> 'Pet':
        return Pet(
            pet_id=self.pet_id if pet_id is EmptyValue else pet_id,
            location=self.location if location is EmptyValue else location,
            accept=self.accept if accept is EmptyValue else accept,
            content=self.content if content is EmptyValue else content,
            specie=self.specie if specie is EmptyValue else specie,
            gender=self.gender if gender is EmptyValue else gender,
            date_birth=self.date_birth if date_birth is EmptyValue else date_birth,
            date_create=self.date_create if date_create is EmptyValue else date_create,
            date_update=self.date_update if date_update is EmptyValue else date_update,
            date_publish=self.date_publish if date_publish is EmptyValue else date_publish,
            page_link=self.page_link if page_link is EmptyValue else page_link,
            photos=self.photos if photos is EmptyValue else photos,
            status=self.status if status is EmptyValue else status,
            user_origin_id=self.user_origin_id if user_origin_id is EmptyValue else user_origin_id,
            user_guard_id=self.user_guard_id if user_guard_id is EmptyValue else user_guard_id,
            user_candidate_ids=self.user_candidate_ids if user_candidate_ids is EmptyValue else user_candidate_ids,
            health_ids=self.health_ids if health_ids is EmptyValue else health_ids,
            hits=self.hits if hits is EmptyValue else hits,
            days_left_expired=self.days_left_expired if days_left_expired is EmptyValue else days_left_expired,
            register_status=self.register_status if register_status is EmptyValue else register_status, )

    def copy_with_photos(self, photo: Photo, ) -> 'Pet':
        if self.photos is None:
            return self.copy_with(
                photos=[photo.copy_with(featured=True, ), ])

        if photo.featured is False:
            return self.copy_with(photos=self.photos + [photo, ], )

        else:
            photos: List[Photo] = []

            for item_photo in self.photos:
                if item_photo.featured is True:
                    item_photo = item_photo.copy_with(featured=False, )

                    photos.append(item_photo, )

            return self.copy_with(photos=photos, )

    def is_limit_photos(self, ) -> bool:
        if self.photos is None:
            return False

        return len(self.photos) >= 3

    def is_active(self, ) -> bool:
        return self.register_status is True

    def is_expired(self, ) -> bool:
        if self.days_left_expired <= 0:
            return True

        return False

    def is_status_needy(self, ) -> bool:
        return self.status.value == PetStatus.STATUS_NEEDY.value

    def is_status_adopt(self, ) -> bool:
        return self.status.value == PetStatus.STATUS_ADOPT.value

    def is_status_origin_adopt(self, ) -> bool:
        return self.status.value == PetStatus.STATUS_ORIGIN_ADOPT.value

    def is_accept(self, ) -> bool:
        if self.accept is None:
            return False

        return self.accept.value == Accept.TRUE.value

    def is_accept_false(self, ) -> bool:
        if self.accept is None:
            return False

        return self.accept.value == Accept.FALSE.value

    def is_accept_pending(self, ) -> bool:
        if self.accept is None:
            return False

        return self.accept.value == Accept.PENDING.value

    def is_accept_revision(self, ) -> bool:
        if self.accept is None:
            return False

        return self.accept.value == Accept.REVISION.value

    def is_valid_for_create(self, user: User, ) -> bool:
        if self.pet_id is not None:
            raise CoreException('pet id must be None.')

        if user.user_id != self.user_origin_id.user_id:
            if not user.is_profile_admin():
                raise CoreException('not permission.')

        if self.status == PetStatus.STATUS_ADOPT:
            raise CoreException('status must be not STATUS_ADOPT.')

        if self.status == PetStatus.STATUS_ORIGIN_ADOPT:
            if self.user_guard_id is None:
                raise CoreException('user_guard_id must be not None.')

            if self.user_guard_id != self.user_origin_id:
                raise CoreException('user_guard_id must be equal user_origin_id.')

            if self.user_origin_id.is_active() is False:
                raise CoreException('user origin must be active.')

            if self.user_guard_id.is_active() is False:
                raise CoreException('user guard must be active.')

        if self.status == PetStatus.STATUS_NEEDY:
            if self.user_origin_id is None:
                raise CoreException('user_origin_id must be not None.')

            if self.user_guard_id is not None:
                raise CoreException('user_guard_id must be None.')

            if self.user_origin_id.is_active() is False:
                raise CoreException('user origin must be active.')

        return is_must_be_empty_for_create(pet=self, )

    def is_valid_for_update(self, user: User, pet_new: 'Pet', ) -> bool:
        if self.pet_id is None or pet_new.pet_id is None:
            raise CoreException('pet id must be not None.')

        if self.pet_id != pet_new.pet_id:
            raise CoreException('pet id must be equal.')

        if self.is_active() is False:
            if not user.is_profile_admin():
                raise CoreException('not permission.')

        if user.user_id != self.user_origin_id.user_id:
            if not user.is_profile_admin():
                raise CoreException('not permission.')

        if self.is_accept_false():
            if not user.is_profile_admin():
                raise CoreException('not permission.')

        if pet_new.date_publish:
            if not user.is_profile_admin():
                raise CoreException('not permission.')

        if self.is_status_needy() and pet_new.status.value not in [PetStatus.STATUS_NEEDY.value,
                                                                   PetStatus.STATUS_ADOPT.value, ]:
            raise CoreException('status must be STATUS_NEEDY or STATUS_ADOPT.')

        if self.is_status_adopt() and not pet_new.is_status_adopt():
            raise CoreException('status must be STATUS_ADOPT')

        if self.is_status_origin_adopt() and not pet_new.is_status_origin_adopt():
            raise CoreException('status must be STATUS_ORIGIN_ADOPT.')

        if self.user_guard_id is None and pet_new.user_guard_id is not None:
            if not self.is_status_needy():
                raise CoreException('status must be STATUS_NEEDY.')

            if pet_new.user_guard_id.is_active() is False:
                raise CoreException('user guard must be active.')

            if pet_new.status != PetStatus.STATUS_ADOPT:
                raise CoreException('status must be STATUS_ADOPT.')

        if self.user_guard_id is not None:
            if pet_new.user_guard_id is None:
                raise CoreException('user_guard_id must be not None.')

            if pet_new.user_guard_id != self.user_guard_id:
                raise CoreException('user_guard_id must be equal.')

        return is_must_be_empty_for_update(pet=pet_new, )
