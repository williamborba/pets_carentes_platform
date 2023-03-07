from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.infrastructure.dataclass_config import DataClassConfig
from app_api.core.infrastructure.types import EmptyValue


class ProviderType(Enum):
    GOOGLE: int = 1
    FACEBOOK: int = 2
    EMAIL: int = 3


class ProfileType(Enum):
    PROTECTOR: int = 1
    COMMON: int = 2
    ADMIN: int = 3


@dataclass(frozen=True, config=DataClassConfig, )
class Provider:
    provider_type: ProviderType
    uid: int
    email: Optional[str] = None
    password: Optional[str] = None
    photo: Optional[str] = None
    name: Optional[str] = None

    def is_provider_email(self) -> bool:
        if self.provider_type == ProviderType.EMAIL:
            return True

        return False


@dataclass(frozen=True, config=DataClassConfig, )
class Profile:
    profile_type: ProfileType
    name: Optional[str] = None
    photo: Optional[str] = None
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    donation: Optional[str] = None


@dataclass(frozen=True, config=DataClassConfig, )
class User:
    provider: Provider
    profile: Profile
    fcm_token: str
    platform: str
    ads: bool
    paid_subscriber: bool
    register_status: bool
    user_id: Optional[str] = None
    chat_user_id_block: Optional[List[str]] = None
    date_create: Optional[datetime] = None
    date_update: Optional[datetime] = None

    def copy_with(self, user_id: Optional[str] = EmptyValue, provider: Optional[Provider] = EmptyValue,
                  profile: Optional[Profile] = EmptyValue, fcm_token: Optional[str] = EmptyValue,
                  platform: Optional[str] = EmptyValue, ads: Optional[bool] = EmptyValue,
                  paid_subscriber: Optional[bool] = EmptyValue, chat_user_id_block: Optional[List] = EmptyValue,
                  date_create: Optional[datetime] = EmptyValue, date_update: Optional[datetime] = EmptyValue,
                  register_status: Optional[bool] = EmptyValue):
        return User(
            user_id=self.user_id if user_id is EmptyValue else user_id,
            provider=self.provider if provider is EmptyValue else provider,
            profile=self.profile if profile is EmptyValue else profile,
            fcm_token=self.fcm_token if fcm_token is EmptyValue else fcm_token,
            platform=self.platform if platform is EmptyValue else platform,
            ads=self.ads if ads is EmptyValue else ads,
            paid_subscriber=self.paid_subscriber if paid_subscriber is EmptyValue else paid_subscriber,
            chat_user_id_block=self.chat_user_id_block if chat_user_id_block is EmptyValue else chat_user_id_block,
            date_create=self.date_create if date_create is EmptyValue else date_create,
            date_update=self.date_update if date_update is EmptyValue else date_update,
            register_status=self.register_status if register_status is EmptyValue else register_status)

    def is_active(self) -> bool:
        return self.register_status is True

    def is_profile_admin(self) -> bool:
        if self.profile.profile_type == ProfileType.ADMIN:
            return True

        return False

    def is_profile_protector(self) -> bool:
        if self.profile.profile_type == ProfileType.PROTECTOR:
            return True

        return False

    def is_valid_provider_email_with_password(self) -> bool:
        if self.provider.provider_type == ProviderType.EMAIL and self.provider.password is None:
            raise CoreException('if provider is email then password is required.')

        return True

    def is_valid(self) -> bool:
        return self.is_valid_provider_email_with_password()
