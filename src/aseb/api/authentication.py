from django.apps import apps
from rest_framework import authentication, exceptions


class TokenAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"

    def get_model(self):
        return apps.get_model("users.AccessToken")

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related("user").get(token=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token.")

        if not token.is_valid():
            raise exceptions.AuthenticationFailed("Token expired.")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return (token.user, token)
