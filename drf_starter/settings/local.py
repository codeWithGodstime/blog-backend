from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

AWS_ACCESS_KEY_ID = env("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = "localhost:9444/ui/mesh"
AWS_S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "endpoint_url": AWS_S3_ENDPOINT_URL,
#             "use_ssl": True,
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "endpoint_url": AWS_S3_ENDPOINT_URL,
#             "use_ssl": True,
#         },
#     },
# }

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}