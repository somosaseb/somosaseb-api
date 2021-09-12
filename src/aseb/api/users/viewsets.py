from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, permissions
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

    @swagger_auto_schema(request_body=UserUpdateSerializer, responses={200: UserSerializer()})
    def create(self, request):
        serializer = UserUpdateSerializer(
            context={"request": request},
            data=request.data,
            instance=request.user,
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(UserSerializer(context={"request": request}).to_representation(user))


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    model = User

    def get_queryset(self):
        return User.objects.all()
