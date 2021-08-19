from django.core.validators import RegexValidator
from django.db import models

from aseb.core.db.fields import UUIDPrimaryKey
from aseb.core.db.models.base import AuditedModel, User, ContactModel, WebPageModel

emoji_validator = RegexValidator(
    r"(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])"
)


class Interest(models.Model):
    name = models.CharField(max_length=100)
    emoji = models.CharField(validators=[emoji_validator], max_length=1)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Market(models.Model):
    name = models.CharField(max_length=100)
    sibling = models.ManyToManyField("self", blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Company(AuditedModel, ContactModel, WebPageModel):
    class Size(models.IntegerChoices):
        S1 = 1, "1 - 4 employees"
        S2 = 2, "5 - 9 employees"
        S3 = 3, "10 - 19 employees"
        S4 = 4, "20 - 49 employees"
        S5 = 5, "50 - 99 employees"
        S6 = 6, "100 - 249 employees"
        S7 = 7, "250 - 499 employees"
        S8 = 8, "500 - 999 employees"
        S9 = 9, "1,000+ employees"

    headline = models.CharField(max_length=140, blank=True)
    presentation = models.TextField(blank=True)
    markets = models.ManyToManyField(Market, verbose_name="Market's of interest")
    size = models.IntegerField(choices=Size.choices, blank=True, null=True)

    class Meta:
        verbose_name_plural = "companies"


class Member(AuditedModel, ContactModel, WebPageModel):
    class Type(models.TextChoices):
        MEMBER = "member", "Member"
        PARTNER_INDIVIDUAL = "partnerIndividual", "Individual Partner"
        PARTNER_CORPORATE = "partnerCorporate", "Corporate Partner"

    class Position(models.TextChoices):
        PRESIDENT = "president", "President"
        ADVISOR = "advisor", "Advisor"
        BOARD_MEMBER = "boardMember", "Board Member"

    id = UUIDPrimaryKey()
    login = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=140, blank=True)
    last_name = models.CharField(max_length=140, blank=True)
    display_name = models.CharField(max_length=140, blank=True)

    headline = models.CharField(max_length=140, blank=True)
    presentation = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    position = models.CharField(max_length=20, choices=Position.choices, blank=True, null=True)

    interests = models.ManyToManyField(Interest, blank=True)
    markets = models.ManyToManyField(Market, verbose_name="Market's of interest", blank=True)
    company = models.ForeignKey(
        Company,
        related_name="members",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    nominated_by = models.ForeignKey(
        "self",
        related_name="nominated_members",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    activated_at = models.DateField(blank=True, null=True)
    expires_at = models.DateField(blank=True, null=True)
