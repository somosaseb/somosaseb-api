import secrets
import string
from functools import partial

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from aseb.core.db.utils import UploadToFunction


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


user_avatar_upload = UploadToFunction("avatars/{obj.pk}.{ext}")

get_random_secret_key = partial(
    get_random_string,
    allowed_chars=string.ascii_lowercase + string.digits + "-_=+",
    length=42,
)
get_random_username = partial(
    get_random_string,
    allowed_chars="123456789",  # We ignore 0 to avoid usernames that starts with it..
    length=16,
)


class User(AbstractUser):
    username = models.CharField(
        "username",
        max_length=50,
        blank=True,
        help_text="Required. 50 characters or fewer. Letters, digits and -/_ only.",
        validators=[RegexValidator(r"^[\w_\-.]+\Z")],
    )

    avatar = models.ImageField(upload_to=user_avatar_upload, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    secret_key = models.CharField(max_length=42, default=get_random_secret_key)
    jwt_jti = models.CharField(max_length=256, blank=True, editable=False)

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

    def save(self, **kwargs):
        if not self.username:
            # Random unique username, could be useful for later as an alternative to ID's
            self.username = get_random_username()

            while User.objects.filter(username=self.username).exists():
                self.username = get_random_username()

        super().save(**kwargs)


class AccessToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=255, unique=True)
    expires = models.DateTimeField(null=True)
    scope = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token

    def is_valid(self, scopes=None):
        return not self.is_expired() and self.allow_scopes(scopes)

    def is_expired(self):
        if self.expires:
            return now() >= self.expires

        return False

    def allow_scopes(self, scopes):
        if not scopes:
            return True
        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)

    def revoke(self):
        self.delete()

    @property
    def scopes(self):
        all_scopes = {}  # TODO: Implement scopes?
        token_scopes = self.scope.split()
        return {name: desc for name, desc in all_scopes.items() if name in token_scopes}

    def save(self, **kwargs):
        if not self.id:
            self.token = secrets.token_urlsafe(60)

        super().save(**kwargs)
