import io
import traceback
import uuid

import PIL.Image
import boto3
from kink import inject

from app_api.core.exceptions.core_exception import CoreException
from app_api.core.settings import Settings


@inject
class S3UploadPhotoService:
    settings: Settings

    def __init__(self, settings: Settings, ):
        self.settings = settings

    async def __call__(self, asset: bytes, size_w: int = 1024, size_h: int = 1024, quality: int = 75, ) -> str:
        try:
            asset_stream: PIL.Image.Image = PIL.Image.open(io.BytesIO(asset), 'r')
            asset_stream = asset_stream.resize((size_w, size_h), PIL.Image.ANTIALIAS)
            asset_byte = io.BytesIO()
            asset_stream.save(asset_byte, format='webp', quality=quality)

            asset_name: str = '%s.webp' % (uuid.uuid4().__str__(),)
            s3 = boto3.client(
                's3', aws_access_key_id=self.settings.aws_key,
                aws_secret_access_key=self.settings.aws_secret,
                region_name=self.settings.aws_s3_region)

            s3.put_object(
                ACL='public-read',
                Bucket=self.settings.aws_s3_bucket,
                Key=asset_name,
                Body=asset_byte.getvalue(),
                ContentType='image/webp')

            return asset_name

        except Exception:
            raise CoreException(message=traceback.format_exc().splitlines().__str__())
