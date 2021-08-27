import rest_framework_filters as filters
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, parsers, permissions

from aseb.api import viewsets
from aseb.api.members.serializers import (
    MemberRetrieveSerializer,
    MemberSerializer,
    MemberUpdateSerializer,
)
from aseb.api.mixins import CountModelMixin
from aseb.apps.organization.models import Member
from aseb.core.exceptions import ResponseException


class MemberFilter(filters.FilterSet):
    birthday = filters.DateRangeFilter()

    class Meta:
        model = Member
        fields = (
            "type",
            "slug",
            "birthday",
            "position",
            "visibility",
            "activated_at",
            "expires_at",
            "partner_since",
        )


@method_decorator(
    name="update",
    decorator=swagger_auto_schema(responses={200: MemberSerializer()}),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(responses={200: MemberSerializer()}),
)
class MemberViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    CountModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
    serializer_class = MemberSerializer
    serializers_classes = {
        "retrieve": MemberRetrieveSerializer,
        "update": MemberUpdateSerializer,
        "partial_update": MemberUpdateSerializer,
    }

    filter_class = MemberFilter
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Member.objects.public()

        queryset = Member.objects.prefetch_related("topics")

        return queryset.filter(
            Q(login=self.request.user) | ~Q(visibility=Member.Visibility.PRIVATE)
        )

    def check_object_permissions(self, request, obj):
        if self.action in {"update", "partial_update"}:
            return obj.login == request.user

        return super().check_object_permissions(request, obj)

    def perform_update(self, serializer):
        obj = serializer.save()

        if obj.slug != self.kwargs["slug"]:
            # Redirect to the new member url
            raise ResponseException(redirect("member-detail", obj.slug))
