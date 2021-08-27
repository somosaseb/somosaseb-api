from rest_framework import serializers

from aseb.apps.organization.models import Company, Member


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
    class MemberInterestSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source="interest__name")
        emoji = serializers.CharField(source="interest__emoji")

        class Meta:
            model = Member.interests.through
            fields = ("name", "emoji")

    class MemberMarketSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source="market__name")

        class Meta:
            model = Member.markets.through
            fields = ("name",)

    url = serializers.HyperlinkedIdentityField(
        view_name="member-detail",
        lookup_field="slug",
    )

    company = CompanySerializer(read_only=True)
    type = serializers.ReadOnlyField()
    position = serializers.ReadOnlyField()
    interests = MemberInterestSerializer(read_only=True, many=True)
    markets = MemberMarketSerializer(read_only=True, many=True)

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
            "interests",
            "markets",
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
    interests = MemberSerializer.MemberInterestSerializer(read_only=True, many=True)
    markets = MemberSerializer.MemberMarketSerializer(read_only=True, many=True)
    nominated_by = MemberNominatedBySerializer(read_only=True, many=True)

    mentor_interests = MemberSerializer.MemberInterestSerializer(read_only=True, many=True)
    mentor_presentation = MemberSerializer.MemberMarketSerializer(read_only=True, many=True)

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
            "interests",
            "markets",
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
            "mentor_interests",
            "mentor_presentation",
        )


class MemberUpdateSerializer(serializers.ModelSerializer):
    class MemberUpdateInterestSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source="interest__name")
        emoji = serializers.CharField(source="interest__emoji")

        class Meta:
            model = Member.interests.through
            fields = ("name", "emoji")

    class MemberUpdateMarketSerializer(serializers.ModelSerializer):
        name = serializers.CharField(source="market__name")

        class Meta:
            model = Member.interests.through
            fields = ("name",)

    interests = MemberUpdateInterestSerializer(read_only=True, many=True)
    markets = MemberUpdateMarketSerializer(read_only=True, many=True)

    class Meta:
        model = Member
        fields = (
            "slug",
            "main_image",
            # Profile
            "first_name",
            "last_name",
            "birthday",
            "display_name",
            "headline",
            "presentation",
            "contact",
            "interests",
            "markets",
        )

    def to_representation(self, instance):
        return MemberSerializer().to_representation(instance)
