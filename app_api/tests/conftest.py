from starlette.config import environ

from app_api.core.settings import ENV_TEST

environ['ENV'] = ENV_TEST
