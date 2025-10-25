from .base import *
import os
import dj_database_url

# Security
DEBUG = False
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Database
DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL"),
        conn_max_age=600, 
        ssl_require=False, #
    )
}
# CORS
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")

# Storage
AWS_ACCESS_KEY_ID = env("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = "localhost:9444/ui/mesh"
AWS_S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")

STORAGES = {
    "default": {
        "BACKEND": "drf_starter.storage_backends.PublicMediaStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "use_ssl": True,
        },
    },
    "staticfiles": {
        "BACKEND": "drf_starter.storage_backends.StaticStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "use_ssl": True,
        },
    },
}

# ------------------------
# Static & Media URLs
# ------------------------
STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/"
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/"
# STATIC_ROOT = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/staticfiles/"

# ------------------------
# CKEditor
# ------------------------
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")