from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS", "*")  # noqa:

DATABASES["default"]["CONN_MAX_AGE"] = env("CONN_MAX_AGE", 60)  # noqa:
