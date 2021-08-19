from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env("CONN_MAX_AGE")
