from dataclasses import dataclass

from kink import di
from starlette.config import Config

ENV_RUNTIME = 'RUNTIME'
ENV_SANDBOX = 'SANDBOX'
ENV_TEST = 'TEST'


@dataclass(frozen=True)
class Settings:
    env: str
    jwt_secret: str
    api_secret: str
    database_primary_host: str
    database_primary_port: int
    database_primary_name: str
    database_primary_username: str
    database_primary_password: str
    database_queue_host: str
    database_queue_port: int
    database_queue_password: str
    sentry_dsn: str
    aws_key: str
    aws_secret: str
    aws_s3_region: str
    aws_s3_bucket: str
    aws_s3_url_prefix: str


def config_di(path_root: str) -> None:
    config: Config = Config(f'{path_root}/.env')

    di[Settings] = Settings(
        env=config('ENV', cast=str, default=ENV_RUNTIME, ),
        jwt_secret=config('JWT_SECRET', cast=str, default='', ),
        api_secret=config('API_SECRET', cast=str, default='', ),
        database_primary_host=config('DATABASE_PRIMARY_HOST', cast=str, ),
        database_primary_port=config('DATABASE_PRIMARY_PORT', cast=int, ),
        database_primary_name=config('DATABASE_PRIMARY_NAME', cast=str, ),
        database_primary_username=config('DATABASE_PRIMARY_USERNAME', cast=str, ),
        database_primary_password=config('DATABASE_PRIMARY_PASSWORD', cast=str, ),
        database_queue_host=config('DATABASE_QUEUE_HOST', cast=str, ),
        database_queue_port=config('DATABASE_QUEUE_PORT', cast=int, ),
        database_queue_password=config('DATABASE_QUEUE_PASSWORD', cast=str, ),
        sentry_dsn=config('SENTRY_DSN', cast=str, ),
        aws_key=config('AWS_KEY', cast=str, ),
        aws_secret=config('AWS_SECRET', cast=str, ),
        aws_s3_region=config('AWS_S3_REGION', cast=str, ),
        aws_s3_bucket=config('AWS_S3_BUCKET', cast=str, ),
        aws_s3_url_prefix=config('AWS_S3_URL_PREFIX', cast=str, ),
    )
