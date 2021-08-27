import rest_framework_filters as filters
from rest_framework import mixins, serializers

from aseb.api.mixins import CountModelMixin
from aseb.api.viewsets import GenericViewSet
from aseb.apps.organization.models import Topic


class MemberFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    prefix = filters.ChoiceFilter(
        choices=(
            ("interest", "Interest"),
            ("market", "Market"),
        ),
        required=True,
        method="filter_prefix",
    )

    class Meta:
        model = Topic
        fields = (
            "prefix",
            "name",
        )

    def filter_prefix(self, queryset, name, value):
        return queryset.filter(name__istartswith=f"{value} / ")


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("name", "emoji")


class TopicViewSet(
    mixins.ListModelMixin,
    CountModelMixin,
    GenericViewSet,
):
    model = Topic
    serializer_class = TopicSerializer
    filter_class = MemberFilter

    # There are no needs to protect this endpoint
    authentication_classes = ()
    permission_classes = ()

    # This view will be mainly a search and look, so no pagination is needed
    pagination_class = None
    max_results: int = 40

    def get_queryset(self):
        if self.request.GET.get("prefix", None) is None:
            return Topic.objects.none()

        return Topic.objects.filter()

    def filter_queryset(self, queryset):
        return queryset[: self.max_results]
