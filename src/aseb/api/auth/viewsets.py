from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from aseb.api import viewsets
from aseb.apps.users.models import User

from ..users.serializers import UserSerializer
from .serializers import RegisterSerializer


class AuthViewSet(viewsets.ViewSet):
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD
                ),
            },
        ),
    )
    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data["user"]
        user.tokens.all().delete()  # TODO: By smart about rotating tokens on every login
        token = user.tokens.create(user=user)

        return Response(
            {
                "token": token.token,
                "expires": token.expires,
                "scopes": token.scopes,
                "user": UserSerializer().to_representation(user),
            }
        )

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
            )
        },
    )
    @action(methods=["post"], detail=False)
    def register(self, request, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer().to_representation(user))
