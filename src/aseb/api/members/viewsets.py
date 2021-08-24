import rest_framework_filters as filters
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, parsers, permissions

from aseb.api import viewsets
from aseb.api.members.serializers import MemberSerializer, MemberUpdateSerializer
from aseb.api.mixins import CountModelMixin
from aseb.apps.organization.models import Member


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
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = MemberSerializer
    serializers_classes = {
        "update": MemberUpdateSerializer,
        "partial_update": MemberUpdateSerializer,
    }

    filter_class = MemberFilter
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        try:
            membership = self.request.user.membership
        except ObjectDoesNotExist:
            membership = None

        if membership and membership.type == Member.Type.PARTNER:
            # ALlow partners to see other partners
            return Member.objects.filter(
                ~Q(visibility=Member.Visibility.PRIVATE),
                Q(type=Member.Type.PARTNER),
            )

        return Member.objects.filter(visibility=Member.Visibility.PUBLIC)

    def check_object_permissions(self, request, obj):
        if self.action in {"update", "partial_update"}:
            return obj.login == request.user

        return super().check_object_permissions(request, obj)
