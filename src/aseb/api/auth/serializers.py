from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework.settings import api_settings

from aseb.apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = (
            User.USERNAME_FIELD,
            "password",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**self.validated_data)
        return user
