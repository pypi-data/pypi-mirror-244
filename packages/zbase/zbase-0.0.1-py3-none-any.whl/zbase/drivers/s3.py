from ..env import getEnv, getEnvBool
from minio import Minio
from typing import BinaryIO
from io import BytesIO
from minio.helpers import ObjectWriteResult
from minio.datatypes import Object
import os

# for testing
# docker run -d -p 9000:9000 -p 9090:9090 --name minio minio/minio server /data --console-address ":9090"
# login with minioadmin:minioadmin 


def bytesIOLen(b:BytesIO)->int:
    pos = b.tell()
    b.seek(0,2)
    size = b.tell()
    b.seek(pos)
    return size

class S3Client:

    def __init__(self,endpoint:str=getEnv('S3_ENDPOINT') , bucket:str = getEnv("S3_BUCKET"), accessKey:str=getEnv('S3_ACCESS_KEY'), secretKey:str=getEnv('S3_SECRET_KEY'), region=getEnv("S3_REGION") ,secure=getEnvBool("S3_SECURE",False),check_cert=getEnvBool("S3_CERT_CHECK",False),**kwargs):
        self.client = Minio(
            endpoint,
            access_key=accessKey,
            secret_key=secretKey,
            secure=secure,
            region=region,
            cert_check=check_cert,
            **kwargs
        )
        self.bucket = bucket

    
    def ensureBucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def formatKey(self, key:str)->str:
        return key.lstrip('/').strip()


    def put(self, key:str, src:str|BinaryIO|bytes, content_type=None)->ObjectWriteResult:
        """
        @param src: str|BinaryIO|bytes , str is file path , BinaryIO is file object by open('file','rb') , bytes is file content
        @param content_type: str

        """
        key = self.formatKey(key)
        if isinstance(src, str):
            return self.client.fput_object(self.bucket, key, src, content_type)
        if isinstance(src, bytes):
            return self.client.put_object(self.bucket, key, BytesIO(src),length=len(src), content_type=content_type)
        if isinstance(src, BytesIO):
            return self.client.put_object(self.bucket, key, src,length=bytesIOLen(src), content_type=content_type)
        return self.client.put_object(self.bucket, key, src, content_type)
    
    def get(self, key:str)->bytes:
        key = self.formatKey(key)
        with self.client.get_object(self.bucket, key) as resp:
            return resp.read()

    def download(self, key:str, dst:str)->Object:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        key = self.formatKey(key)
        return self.client.fget_object(self.bucket, key, dst)

    def stat(self, key:str)->Object:
        key = self.formatKey(key)
        return self.client.stat_object(self.bucket, key)
    
    def remove(self, key:str):
        key = self.formatKey(key)
        return self.client.remove_object(self.bucket, key)
    