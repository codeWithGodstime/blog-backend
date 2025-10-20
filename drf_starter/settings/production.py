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
        ssl_require=True, 
    )
}
# CORS
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")

# ------------------------
# Static & Media via S3
# ------------------------
AWS_ACCESS_KEY_ID = env("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = env("S3_REGION", default=None)
AWS_QUERYSTRING_AUTH = False  # so URLs are public
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False

# Default (user uploads)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Static (collected files)
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# These URLs are automatically built by django-storages, don't prefix manually
STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/static/"
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/media/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ------------------------
# CKEditor
# ------------------------
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

# This ensures CKEditor JS resolves to the correct S3 static path
CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")