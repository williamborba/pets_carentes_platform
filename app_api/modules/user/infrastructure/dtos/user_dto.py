from datetime import datetime
from typing import List, Dict, Optional

from bson.objectid import ObjectId
from pydantic.dataclasses import dataclass

from app_api.core.infrastructure.dataclass_config import DataClassConfig
from app_api.modules.user.entitys.user import \
    Provider, Profile, User, ProviderType, ProfileType


@dataclass(frozen=True, config=DataClassConfig, )
class ProviderDto:
    provider_type: ProviderType
    uid: int
    email: Optional[str] = None
    password: Optional[str] = None
    photo: Optional[str] = None
    name: Optional[str] = None

    @staticmethod
    def from_json(data: Dict) -> 'ProviderDto':
        return ProviderDto(
            provider_type=ProviderType(value=data.get('provider_type')),
            uid=data.get('uid'),
            email=data.get('email', None),
            password=data.get('password', None),
            photo=data.get('photo', None),
            name=data.get('name', None), )

    @staticmethod
    def from_entity(provider: Provider) -> 'ProviderDto':
        return ProviderDto(
            provider_type=provider.provider_type,
            uid=provider.uid,
            email=provider.email,
            password=provider.password,
            photo=provider.photo,
            name=provider.name, )

    def to_json(self) -> Dict:
        return {
            'provider_type': self.provider_type.value,
            'uid': self.uid,
            'email': self.email,
            'password': self.password,
            'photo': self.photo,
            'name': self.name
        }

    def to_entity(self) -> Provider:
        return Provider(
            provider_type=self.provider_type,
            uid=self.uid,
            email=self.email,
            password=self.password,
            photo=self.photo,
            name=self.name)


@dataclass(frozen=True, config=DataClassConfig, )
class ProfileDto:
    profile_type: ProfileType
    name: Optional[str] = None
    photo: Optional[str] = None
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    donation: Optional[str] = None

    @staticmethod
    def from_json(data: Dict) -> 'ProfileDto':
        return ProfileDto(
            profile_type=ProfileType(value=data.get('profile_type')),
            name=data.get('name'),
            photo=data.get('photo', None),
            whatsapp=data.get('whatsapp', None),
            instagram=data.get('instagram', None),
            facebook=data.get('facebook', None),
            donation=data.get('donation', None), )

    @staticmethod
    def from_entity(profile: Profile) -> 'ProfileDto':
        return ProfileDto(
            profile_type=profile.profile_type,
            name=profile.name,
            photo=profile.photo,
            whatsapp=profile.whatsapp,
            instagram=profile.instagram,
            facebook=profile.facebook,
            donation=profile.donation, )

    def to_json(self) -> Dict:
        return {
            'profile_type': self.profile_type.value,
            'name': self.name,
            'photo': self.photo,
            'whatsapp': self.whatsapp,
            'instagram': self.instagram,
            'facebook': self.facebook,
            'donation': self.donation
        }

    def to_entity(self) -> Profile:
        return Profile(
            profile_type=self.profile_type,
            name=self.name,
            photo=self.photo,
            whatsapp=self.whatsapp,
            instagram=self.instagram,
            facebook=self.facebook,
            donation=self.donation)


@dataclass(frozen=True, config=DataClassConfig, )
class UserDto:
    provider: ProviderDto
    profile: ProfileDto
    fcm_token: str
    platform: str
    ads: bool
    paid_subscriber: bool
    register_status: bool
    user_id: Optional[str] = None
    chat_user_id_block: Optional[List[str]] = None
    date_create: Optional[datetime] = None
    date_update: Optional[datetime] = None

    @staticmethod
    def from_json(data: Dict, object_id: bool = False) -> 'UserDto':
        date_create: Optional[datetime] = None
        date_update: Optional[datetime] = None

        if data.get('date_create', None) is not None:
            date_create = datetime.fromisoformat(data.get('date_create'))

        if data.get('date_update', None) is not None:
            date_update = datetime.fromisoformat(data.get('date_update'))

        return UserDto(
            user_id=data.get('_id', None) if object_id is False else str(ObjectId(data.get('_id', ''))),
            provider=ProviderDto.from_json(data=data.get('provider', {})),
            profile=ProfileDto.from_json(data=data.get('profile', {})),
            fcm_token=data.get('fcm_token'),
            platform=data.get('platform'),
            ads=data.get('ads'),
            paid_subscriber=data.get('paid_subscriber'),
            chat_user_id_block=data.get('chat_user_id_block', None),
            date_create=date_create,
            date_update=date_update,
            register_status=data.get('register_status'), )

    @staticmethod
    def from_entity(user: User) -> 'UserDto':
        return UserDto(
            user_id=user.user_id,
            provider=ProviderDto.from_entity(provider=user.provider),
            profile=ProfileDto.from_entity(profile=user.profile),
            fcm_token=user.fcm_token,
            platform=user.platform,
            ads=user.ads,
            paid_subscriber=user.paid_subscriber,
            chat_user_id_block=user.chat_user_id_block,
            date_create=user.date_create,
            date_update=user.date_update,
            register_status=user.register_status, )

    def to_json(self, without_id: bool = False) -> Dict:
        _data: Dict = {
            '_id': self.user_id,
            'provider': self.provider.to_json(),
            'profile': self.profile.to_json(),
            'fcm_token': self.fcm_token,
            'platform': self.platform,
            'ads': self.ads,
            'paid_subscriber': self.paid_subscriber,
            'chat_user_id_block': self.chat_user_id_block,
            'date_create': self.date_create.isoformat(),
            'date_update': self.date_update.isoformat() if self.date_update is not None else None,
            'register_status': self.register_status
        }

        if without_id:
            _data.pop('_id', None)

        return _data

    def to_entity(self) -> User:
        return User(
            user_id=self.user_id,
            provider=self.provider.to_entity(),
            profile=self.profile.to_entity(),
            fcm_token=self.fcm_token,
            platform=self.platform,
            ads=self.ads,
            paid_subscriber=self.paid_subscriber,
            chat_user_id_block=self.chat_user_id_block,
            date_create=self.date_create,
            date_update=self.date_update,
            register_status=self.register_status, )
