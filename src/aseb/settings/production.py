import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS", "*")  # noqa:

DATABASES["default"]["CONN_MAX_AGE"] = env("CONN_MAX_AGE", 60)  # noqa:

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        LoggingIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
