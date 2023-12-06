import boto3
import botocore
from .io_config import IO_Config


class IO_Reader:
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

    def read(self, path: str, name: str, compress: bool) -> str:
        try:
            if self.cloud_data:
                response_body = self.resource.Object(path, name).get()
                response = response_body["Body"].read()
            else:
                with open(name, "rb") as f:
                    response = f.read()
            return response
        except Exception as e:
            raise e

    def read_string(self, path: str, name: str, compress: bool) -> str:
        try:
            if self.cloud_data:
                response = self.resource.Object(path, name).get()
            else:
                with open(name, "rb") as f:
                    response = {"Body": f}
            return response["Body"].read().decode("utf-8")
        except Exception as e:
            raise e

    def object_exists(self, path: str, object_type: str) -> bool:
        try:
            self.resource.Object(path).load()
        except botocore.exceptions.ClientError:
            return False
        return True
