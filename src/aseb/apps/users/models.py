from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager

from django.utils.crypto import get_random_string


def get_random_secret_key() -> str:
    return get_random_string(length=24)


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username: str):
        if "@" in username:
            return self.get(email__iexact=username)
        return self.get(username__exact=username)

    def create_user(
        self,
        email: str,
        password: str = None,
        is_staff: bool = False,
        is_active: bool = True,
        **extra_fields,
    ):
        email = UserManager.normalize_email(email)
        extra_fields.pop("username", None)

        user = self.model(
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            **extra_fields,
        )

        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(
        self,
        email: str,
        password: str = None,
        **extra_fields,
    ):
        return self.create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )


class User(AbstractUser):
    username = models.CharField(
        "username",
        max_length=150,
        blank=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[AbstractUser.username_validator],
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    secret_key = models.CharField(max_length=24, default=get_random_secret_key)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["date_joined"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>".strip()

    def generate_secret_key(self):
        self.secret_key = get_random_secret_key()
        self.save(update_fields=["secret_key"])
