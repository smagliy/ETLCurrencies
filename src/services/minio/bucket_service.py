from minio import Minio
from minio.error import S3Error
from io import BytesIO

from src.services.logger.logging import LoggerConfig

logger = LoggerConfig.set_up_logger()


class BucketOperations(object):
    def __init__(self, minio_docker_url, minio_access_key, minio_secret_key):
        logger.info(f"Initialized MinIO client")
        self.client = Minio(minio_docker_url,
                            access_key=minio_access_key,
                            secret_key=minio_secret_key,
                            secure=False
                            )

    def write_string_to_bucket(self, bucket, folder_path, file_name, content):
        if not bucket or not folder_path:
            raise ValueError("Bucket name and object path must be specified")
        try:
            converted = BytesIO(content)
            size = converted.getbuffer().nbytes
            self.client.put_object(bucket, f'{folder_path}{file_name}', converted, size)
            logger.info(f"Successfully wrote to {bucket}/{folder_path}")
        except S3Error as e:
            logger.error(f"Failed to write to {bucket}/{folder_path}: {e}")
            raise
