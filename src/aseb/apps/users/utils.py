from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from aseb.apps.users.models import User

AUTHORIZATION_HEADER = "HTTP_AUTHORIZATION"


def get_user_by_email(email: str) -> Optional[User]:
    try:
        return User.objects.get_by_natural_key(email)
    except ObjectDoesNotExist:
        return None


def get_user_by_id(pk: int) -> Optional[User]:
    return User.objects.filter(pk=pk).first()


def user_can_authenticate(user: User) -> bool:
    return user.is_active
