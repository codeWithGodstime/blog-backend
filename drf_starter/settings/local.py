from .base import *
environ.Env.read_env(os.path.join(BASE_DIR, 'env/.env.local'))


LOCAL_APPS = [
    "rest_framework",

    "corsheaders",
    "storages",
]

# Default django app + your local apps
INSTALLED_APPS = BASE_APPS + LOCAL_APPS

AWS_ACCESS_KEY_ID = env("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "localhost:9444/ui/mesh"
AWS_S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")
AWS_S3_USE_SSL = False
AWS_S3_URL_PROTOCOL = "http:"

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "use_ssl": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_URL = 'static/'
MEDIA_URL = f"{AWS_S3_CUSTOM_DOMAIN}/media/" 