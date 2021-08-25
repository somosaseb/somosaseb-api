import string
from functools import partial

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from aseb.apps.users.models import User
from aseb.core.db.fields import EmojiChooseField, PropertiesField
from aseb.core.db.models.base import AuditedModel, WebPageModel
from aseb.core.forms import ContactForm


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    emoji = EmojiChooseField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Market(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sibling = models.ManyToManyField("self", blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


get_profile_slug = partial(get_random_string, allowed_chars=string.digits, length=20)


class ProfileQuerySet(models.QuerySet):
    def public(self):
        return self.filter(visibility=Member.Visibility.PUBLIC)

    def open(self):
        return self.filter(visibility=Member.Visibility.OPEN)

    def private(self):
        return self.filter(visibility=Member.Visibility.PRIVATE)


class ProfileModel(AuditedModel, WebPageModel):
    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        OPEN = "open", "Open"
        PRIVATE = "private", "Private"

    display_name = models.CharField(max_length=140, blank=True)

    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.OPEN,
        blank=True,
        null=True,
    )

    headline = models.CharField(max_length=140, blank=True)
    presentation = models.TextField(blank=True)
    contact = PropertiesField(form_class=ContactForm, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    markets = models.ManyToManyField(Market, verbose_name="Market's of interest", blank=True)
    objects = ProfileQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, **kwargs):
        if not self.slug:
            # Generate a random identifier for the profile.
            self.slug = get_profile_slug()

            while type(self).objects.filter(slug=self.slug).exists():
                self.slug = get_profile_slug()

        super().save(**kwargs)


class Company(ProfileModel):
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

    display_name = models.CharField(max_length=140)
    size = models.IntegerField(choices=Size.choices, blank=True, null=True)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.display_name


class Member(ProfileModel):
    class Type(models.TextChoices):
        MEMBER = "member", "Member"
        PARTNER = "partner", "Partner"

    class Position(models.TextChoices):
        PRESIDENT = "president", "President"
        ADVISOR = "advisor", "Advisor"
        BOARD_MEMBER = "boardMember", "Board Member"

    login = models.OneToOneField(
        User,
        related_name="membership",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    birthday = models.DateField(blank=True, null=True)

    type = models.CharField(max_length=20, choices=Type.choices)

    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        blank=True,
        null=True,
    )

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

    partner_since = models.DateField(blank=True, null=True)
    activated_at = models.DateField(blank=True, null=True)
    expires_at = models.DateField(blank=True, null=True)

    # Mentor Profile
    mentor_since = models.DateTimeField(blank=True, null=True)
    mentor_interests = models.ManyToManyField(Interest, related_name="+", blank=True)
    mentor_presentation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.type}]"


@receiver(post_save, sender=User, dispatch_uid="create_user_memberprofile")
def create_user_memberprofile(sender, instance: User, **kwargs):
    if any(
        (
            not kwargs["created"],
            kwargs["raw"],
            not (kwargs["update_fields"] is None),
        )
    ):
        return

    Member.objects.create(
        login=instance,
        first_name=instance.first_name,
        last_name=instance.last_name,
        contact={"contact_email": instance.email},
        type=Member.Type.MEMBER,
    )
