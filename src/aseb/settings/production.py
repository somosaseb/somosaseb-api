import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS", "*")  # noqa: F405

DATABASES["default"]["CONN_MAX_AGE"] = env("CONN_MAX_AGE", 60)  # noqa: F405

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),  # noqa: F405
    integrations=[
        DjangoIntegration(),
        LoggingIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Common settings for using gmail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587

# Keep them secret!
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # noqa: F405
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # noqa: F405
