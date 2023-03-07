import traceback

import boto3

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings


class S3DeleteService:
    settings: Settings

    def __init__(self, settings: Settings, ):
        self.settings = settings

    async def __call__(self, asset: str) -> bool:
        try:
            s3 = boto3.client(
                's3', aws_access_key_id=self.settings.aws_key,
                aws_secret_access_key=self.settings.aws_secret,
                region_name=self.settings.aws_s3_region)

            s3.delete_object(
                Bucket=self.settings.aws_s3_bucket,
                Key=asset)

        except Exception:
            raise CoreException(message=traceback.format_exc().splitlines().__str__())

        return True
