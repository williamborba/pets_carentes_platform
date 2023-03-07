import sentry_sdk
from kink import inject

from app_api.core.settings import Settings


@inject
class SentryService:
    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

        sentry_sdk.init(
            dsn=self.settings.sentry_dsn,
            sample_rate=1.0,
            traces_sample_rate=1.0,
            _experiments={
                "profiles_sample_rate": 1.0,
            },
        )
