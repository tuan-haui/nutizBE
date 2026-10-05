import boto3
import os
import logging
from botocore.exceptions import ClientError
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE
        
        if self.storage_type == "s3":
            self.s3_client = boto3.client(
                's3',
                endpoint_url=settings.S3_ENDPOINT_URL,
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY
            )
            self.bucket_name = settings.S3_BUCKET
            
    def upload_file(self, file_path: str, object_name: Optional[str] = None) -> Optional[str]:
        if self.storage_type == "local":
            return file_path
            
        if object_name is None:
            object_name = os.path.basename(file_path)
            
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            
            # Generate pre-signed URL
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=3600
            )
            
            # Optionally cleanup local file here
            try:
                os.remove(file_path)
            except OSError:
                pass
                
            return url
        except ClientError as e:
            logger.error(f"Failed to upload to S3: {e}")
            return None

storage_service = StorageService()
