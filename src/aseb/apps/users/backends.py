from pprint import pprint
from typing import Optional

from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.http import HttpRequest

from aseb.apps.users.models import User
from aseb.apps.users.utils import get_user_by_email, get_user_by_id, user_can_authenticate


class PermissionMixin:
    def get_user(self, user_id: int) -> Optional[User]:
        return get_user_by_id(user_id)

    def get_user_permissions(self, user_obj: User, obj=None) -> set:
        return ModelBackend().get_user_permissions(user_obj, obj)

    def get_group_permissions(self, user_obj: User, obj=None) -> set:
        return ModelBackend().get_group_permissions(user_obj, obj)

    def get_all_permissions(self, user_obj: User, obj=None) -> set:
        return {
            *self.get_user_permissions(user_obj, obj=obj),
            *self.get_group_permissions(user_obj, obj=obj),
        }

    def has_perm(self, user_obj, perm, obj=None) -> bool:
        if user_obj.is_active:
            return BaseBackend().has_perm(user_obj, perm, obj)
        return False


class AuthBackend(PermissionMixin):
    def authenticate(
        self,
        request: HttpRequest,
        username: str,
        password: str,
    ) -> Optional[User]:
        pprint(locals(), indent=2)

        if password == "":
            return None

        user = get_user_by_email(username)

        if user is None:
            User().set_password(password)

            return None

        if user.check_password(password) and user_can_authenticate(user):
            return user

        return None
