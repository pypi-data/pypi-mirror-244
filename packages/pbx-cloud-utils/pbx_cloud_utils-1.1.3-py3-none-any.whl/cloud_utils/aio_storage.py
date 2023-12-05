import datetime
import os
from abc import ABC, abstractmethod
from typing import Any, Tuple

from aiobotocore import config as s3_config
from azure.storage.blob import BlobSasPermissions, generate_blob_sas
from azure.storage.blob.aio import BlobClient, ContainerClient

from cloud_utils.types import S3AddressingStyles
from cloud_utils.utils import get_account_key

try:
    import aiobotocore  # type: ignore

    HAS_AIOBOTOCORE = True
except ImportError:  # pragma: no cover
    HAS_AIOBOTOCORE = False


class AsyncStorage(ABC):
    def __init__(self, bucket_name: str, region_name: str, **kwargs: Any):
        self.region_name: str = region_name
        self.bucket_name: str = bucket_name
        self.extra_kwargs: Any = kwargs

    @abstractmethod
    async def delete_object(self, key: str):
        pass  # pragma: no cover

    @abstractmethod
    async def generate_presigned_url(
        self, key: str, size: str, content_md5: str, **kwargs: Any
    ) -> Tuple[str, dict]:
        pass  # pragma: no cover


class AsyncAmazonS3Storage(AsyncStorage):
    def __new__(cls, *args, **kwargs):
        if not HAS_AIOBOTOCORE:  # pragma: no cover
            raise ImportError("Required aiobotocore, please install aiobotocore>=1.4.0.")
        return super().__new__(cls)

    async def delete_object(self, key: str):
        session = aiobotocore.session.get_session()
        async with session.create_client("s3", self.region_name) as client:
            await client.delete_object(Bucket=self.bucket_name, Key=key)

    async def generate_presigned_url(
        self,
        key: str,
        size: str,
        content_md5: str,
        addressing_style: S3AddressingStyles = "path",
        **kwargs: Any,
    ) -> Tuple[str, dict]:
        headers = {"Content-Length": str(size), "Content-MD5": content_md5}
        session = aiobotocore.session.get_session()
        config = s3_config.AioConfig(s3={"addressing_style": addressing_style})
        async with session.create_client(
            "s3",
            region_name=self.region_name,
            config=config,
            **self.extra_kwargs,
        ) as client:
            url = await client.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                    "ContentLength": size,
                    "ContentMD5": content_md5,
                },
            )

            return url, headers


class AsyncAzureBlobStorage(AsyncStorage):
    def __init__(self, container_name: str, **kwargs: Any) -> None:
        connection_string = kwargs.get(
            "conn_str",
            os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
        )
        self.account_key: str = get_account_key(connection_string)
        self.container_name: str = container_name
        self.client: ContainerClient = ContainerClient.from_connection_string(
            conn_str=connection_string, container_name=container_name
        )

    async def delete_object(self, key: str):
        await self.client.delete_blob(key)

    async def generate_presigned_url(
        self, key: str, size: str, content_md5: str, **kwargs: Any
    ) -> Tuple[str, dict]:
        headers = {
            "x-ms-version": "2021-04-10",
            "x-ms-blob-type": "BlockBlob",
        }
        sas_token = generate_blob_sas(
            account_name=self.client.account_name,
            container_name=self.container_name,
            blob_name=key,
            account_key=self.account_key,
            permission=BlobSasPermissions(create=True, write=True),
            expiry=datetime.datetime.now() + datetime.timedelta(hours=kwargs.get("expiry", 1)),
        )
        container_blob_url = self.client.get_blob_client(key).url
        blob_client = BlobClient.from_blob_url(container_blob_url, credential=sas_token)

        return blob_client.url, headers
