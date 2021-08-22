from rest_framework import serializers

from aseb.apps.organization.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "display_name", "type")
