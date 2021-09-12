from oauth2_provider import views
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


class AuthorizationView(views.AuthorizationView):
    ...


@method_decorator(name="post", decorator=swagger_auto_schema(tags=["tokens"]))
class TokenView(APIView, views.TokenView):
    ...


@method_decorator(name="post", decorator=swagger_auto_schema(tags=["tokens"]))
class RevokeTokenView(APIView, views.RevokeTokenView):
    ...


@method_decorator(name="get", decorator=swagger_auto_schema(tags=["tokens"]))
@method_decorator(name="post", decorator=swagger_auto_schema(tags=["tokens"]))
class IntrospectTokenView(APIView, views.IntrospectTokenView):
    ...


@method_decorator(name="delete", decorator=swagger_auto_schema(tags=["tokens"]))
class AuthorizedTokenDeleteView(APIView, views.AuthorizedTokenDeleteView):
    ...


@method_decorator(name="get", decorator=swagger_auto_schema(tags=["tokens"]))
class AuthorizedTokensListView(APIView, views.AuthorizedTokensListView):
    ...
