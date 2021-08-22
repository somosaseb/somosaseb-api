import rest_framework_filters as filters
from rest_framework import permissions

from aseb.api import viewsets
from aseb.api.members.serializers import MemberSerializer
from aseb.apps.organization.models import Member


class MemberFilter(filters.FilterSet):
    class Meta:
        model = Member
        fields = (
            "type",
            "slug",
            "birthday",
            "position",
            "activated_at",
            "expires_at",
            "partner_since",
        )


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    serializer_class = MemberSerializer
    filter_class = MemberFilter

    def get_queryset(self):
        return Member.objects.all()
