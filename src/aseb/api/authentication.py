from rest_framework import authentication, exceptions

from aseb.apps.users.models import AccessToken


class TokenAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
    model = AccessToken

    def authenticate_credentials(self, key):

        try:
            token = AccessToken.objects.select_related("user").get(token=key)
        except AccessToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token.")

        if not token.is_valid():
            raise exceptions.AuthenticationFailed("Token expired.")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return (token.user, token)
