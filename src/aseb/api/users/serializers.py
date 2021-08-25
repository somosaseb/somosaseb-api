from rest_framework import serializers

from aseb.apps.organization.models import Member
from aseb.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class MembershipSerializer(serializers.HyperlinkedModelSerializer):
        url = serializers.HyperlinkedIdentityField(
            view_name="member-detail",
            lookup_field="slug",
        )

        class Meta:
            model = Member
            fields = ("url", "type", "visibility")

    membership = MembershipSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "is_staff",
            "is_active",
            "date_joined",
            "membership",
        )

    def get_membership(self, instance):
        return instance.membership.all().first()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
        )
