import boto3
import botocore
from .io_config import IO_Config


class IO_Writer:
    def __init__(self, settings: IO_Config) -> None:
        try:
            config = settings
            self.cloud_data = config.cloud_data
            if self.cloud_data:
                self.resource = boto3.resource(
                    "s3",
                    region_name=config.region_name,
                    aws_access_key_id=config.aws_access_key_id,
                    aws_secret_access_key=config.aws_secret_access_key,
                )
                self.region_name = config.region_name
        except Exception as e:
            raise e

    def write(
        self,
        bucket_name: str,
        path: str,
        body: str,
        compress: bool = False,
        cache: bool = False,
    ) -> bool:
        try:
            if self.cloud_data:
                self.resource.Object(bucket_name, path).put(Body=body)
                return True
            else:
                with open(path, "w") as f:
                    f.write(body)
                f.close()
                return True

        except Exception as e:
            raise e

    def object_exists(self, path: str, object_type: str) -> bool:
        if object_type == "recipe":
            bucket = self.recipes_bucket_name
        else:
            raise ValueError(f"Unknown object type: {object_type}")

        try:
            self.resource.Object(bucket, path).load()
        except botocore.exceptions.ClientError:
            return False
        return True
