from storages.backends.s3boto3 import S3Boto3Storage
from distribution.settings import YANDEX_BUCKET_NAME

# Класс для хранения изображений в облаке яндекса
class ClientDocsStorage(S3Boto3Storage):
    bucket_name = YANDEX_BUCKET_NAME
    file_overwrite = False