from .base import *
import os
import dj_database_url

# Security
DEBUG = False
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

# Database
DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL"),
        conn_max_age=600, 
        ssl_require=True, 
    )
}

# CORS
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(",")

# Storage
# AWS_ACCESS_KEY_ID = env("S3_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = env("S3_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = env("S3_CUSTOM_DOMAIN")
# AWS_S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")
# AWS_S3_USE_SSL = True
# AWS_S3_URL_PROTOCOL = "https:"

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "custom_domain": AWS_S3_CUSTOM_DOMAIN,
#             "endpoint_url": AWS_S3_ENDPOINT_URL,
#             "use_ssl": True,
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }

MEDIA_URL = f"{BASE_DIR}/media/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")