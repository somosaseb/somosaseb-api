import uuid

from django.db import models

from aseb.apps.organization.models import Interest, Market, Member
from aseb.core.db.fields import UUIDPrimaryKey
from aseb.core.db.models.base import AuditedModel, PublishableModel, WebPageModel
from aseb.core.db.utils import UploadToFunction

event_image_upload = UploadToFunction("events/{obj.pk}/{filename}.{ext}")


class Serie(AuditedModel, WebPageModel):
    ...


class Event(PublishableModel, AuditedModel, WebPageModel):
    class LocationType(models.TextChoices):
        PLACE = "place", "Place"
        VIRTUAL = "virtual", "Virtual"

    class Audience(models.TextChoices):
        PUBLIC = "public", "Public"
        MEMBERS = "members", "Member"
        PARTNERS = "partners", "Partners"

    id = UUIDPrimaryKey()
    headline = models.CharField(max_length=140, blank=True)
    presentation = models.TextField(blank=True)

    interests = models.ManyToManyField(Interest, blank=True)
    markets = models.ManyToManyField(Market, verbose_name="Market's of interest", blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name="events")

    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)

    audience = models.CharField(choices=Audience.choices, max_length=10)
    capacity = models.IntegerField(blank=True, null=True)

    location_type = models.CharField(choices=LocationType.choices, max_length=10)
    location_address = models.CharField(blank=True, max_length=300)
    location_url = models.URLField(blank=True)


class EventPerformer(models.Model):
    performer = models.ForeignKey(Member, related_name="performed_events", on_delete=models.PROTECT)
    event = models.ForeignKey(Event, related_name="event_performers", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("performer", "event"),)


class EventOrganizer(models.Model):
    organizer = models.ForeignKey(Member, related_name="organized_events", on_delete=models.PROTECT)
    event = models.ForeignKey(Event, related_name="events_organizers", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("organizer", "event"),)
