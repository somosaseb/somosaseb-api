from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from aseb.api import viewsets
from aseb.apps.users.models import User

from .serializers import UserSerializer, UserUpdateSerializer


class CurrentUserViewSet(viewsets.ViewSet):
    parser_classes = (parsers.MultiPartParser,)

    @swagger_auto_schema(responses={200: UserSerializer()})
    def list(self, request):
        return Response(
            UserSerializer(context={"request": request}).to_representation(request.user)
        )

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer()},
    )
    def create(self, request):
        serializer = UserUpdateSerializer(
            context={"request": request},
            data=request.data,
            instance=request.user,
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer().to_representation(user))

    @action(detail=False, methods=["post"])
    def logout(self, request, *args, **kwargs):
        request.user.tokens.all().delete()
        return Response()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    model = User

    def get_queryset(self):
        return User.objects.all()


class AuthToken(viewsets.ViewSet):
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
    def token(self, request, *args, **kwargs):
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
