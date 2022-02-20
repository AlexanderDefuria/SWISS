from abc import ABC

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage, ABC):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    def path(self, name):
        pass

    bucket_name = 'media'
    location = ''
