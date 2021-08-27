from rest_framework import serializers

from aseb.apps.organization.models import Company, Member, Topic
from aseb.core.forms import ContactForm


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "slug",
            "display_name",
            "size",
            "headline",
            "presentation",
            "main_image",
            "contact",
        )


class MemberSerializer(serializers.ModelSerializer):
    class MemberTopicSerializer(serializers.ModelSerializer):
        name = serializers.CharField()

        class Meta:
            model = Member.topics.through
            fields = ("name",)

    url = serializers.HyperlinkedIdentityField(
        view_name="member-detail",
        lookup_field="slug",
    )

    company = CompanySerializer(read_only=True)
    type = serializers.ReadOnlyField()
    position = serializers.ReadOnlyField()
    topics = MemberTopicSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = (
            "url",
            "title",
            "main_image",
            # Profile
            "display_name",
            "headline",
            "presentation",
            "contact",
            "topics",
            # Member
            "first_name",
            "last_name",
            "type",
            "position",
            "company",
            "partner_since",
            "activated_at",
            "expires_at",
        )


class MemberRetrieveSerializer(MemberSerializer):
    class MemberNominatedBySerializer(serializers.ModelSerializer):
        class Meta:
            model = Member
            fields = ("slug", "first_name", "last_name", "main_image")

    company = CompanySerializer(read_only=True)
    type = serializers.ReadOnlyField()
    position = serializers.ReadOnlyField()
    topics = MemberSerializer.MemberTopicSerializer(read_only=True, many=True)
    nominated_by = MemberNominatedBySerializer(read_only=True, many=True)

    mentor_topics = MemberSerializer.MemberTopicSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = (
            "slug",
            "title",
            "main_image",
            # Profile
            "display_name",
            "headline",
            "presentation",
            "contact",
            "topics",
            # Member
            "first_name",
            "last_name",
            "type",
            "position",
            "company",
            "nominated_by",
            "partner_since",
            "activated_at",
            "expires_at",
            "mentor_since",
            "mentor_topics",
            "mentor_presentation",
        )


def validate_contact_form(value):
    form = ContactForm(data=value, model_instance=None)

    if form.is_valid():
        return form.cleaned_data

    raise serializers.ValidationError(form.errors)


class MemberUpdateSerializer(serializers.ModelSerializer):
    class MemberUpdateTopicSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source="topic__name")
        emoji = serializers.CharField(source="topic__emoji")

        class Meta:
            model = Member.topics.through
            fields = ("name", "emoji")

    contact = serializers.DictField(validators=[validate_contact_form])
    topics = MemberUpdateTopicSerializer(many=True)

    class Meta:
        model = Member
        fields = (
            "slug",
            "main_image",
            # Profile
            "first_name",
            "last_name",
            "display_name",
            "birthday",
            "headline",
            "presentation",
            "topics",
            "contact",
        )

    def to_representation(self, instance):
        return MemberSerializer(
            context={"request": self.context["request"]},
        ).to_representation(instance)

    def update(self, instance, validated_data):
        topics = validated_data.pop("topics", None)

        if self.partial and "contact" in validated_data:
            validated_data["contact"] = {**validated_data["contact"], **instance.contact}

        instance: Member = super().update(instance, validated_data)

        if not (topics is None):
            topics = [topic["topic__name"] for topic in topics]
            topics = Topic.objects.filter(name__in=topics)
            instance.topics.set(topics, clear=True)

        if instance.login_id:
            # Sync user
            instance.login.first_name = instance.first_name
            instance.login.last_name = instance.last_name
            instance.login.save(update_fields=["first_name", "last_name"])

        return instance
