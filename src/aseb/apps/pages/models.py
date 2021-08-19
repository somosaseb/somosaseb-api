import re

from django.core.validators import RegexValidator
from django.db import models
from django_ltree.models import TreeModel

from aseb.core.db.models.base import AuditedModel, PublishableModel, WebPageModel
from aseb.core.db.utils import UploadToFunction

validate_url = RegexValidator(
    re.compile(r"^/[-\w/]+/$\Z"),
    "Enter a valid “url”. Starting and ending with an slash.",
    "invalid",
)

page_main_image_upload = UploadToFunction("pages/{obj.pk}/{filename}.{ext}")
website_icon_upload = UploadToFunction("websites/{obj.pk}/{filename}.{ext}")


class Page(AuditedModel, PublishableModel, WebPageModel, TreeModel):
    # We disable the Slug field, we are going to use the path field
    slug = models.SlugField(blank=True, editable=True)
    redirect_to = models.URLField(blank=True)

    class Meta:
        ordering = ("path",)

    def root(self):
        return self.path[-1]

    @property
    def url(self):
        return "/" + "/".join(self.path)

    def __str__(self) -> str:
        return self.url

    def get_absolute_url(self) -> str:
        return "/".join(self.path[1:])


class Website(AuditedModel):
    class Status(models.TextChoices):
        PUBLISHED = "publish", "Published"
        PUBLISHING = "publishing", "Publishing"

    class Access(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private, require authentication"

    hostname = models.CharField(max_length=40, unique=True)
    aliases = models.CharField(max_length=140, blank=True)
    name = models.CharField(max_length=140)
    tagline = models.CharField(max_length=140, blank=True)
    description = models.CharField(max_length=280, blank=True)
    icon = models.ImageField(upload_to=website_icon_upload, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED)

    search_description = models.CharField(max_length=140, blank=True)
    allow_searchengine = models.BooleanField(verbose_name="Visible to search engines")

    reader_access = models.CharField(max_length=10, choices=Access.choices, default=Access.PUBLIC)
    custom_robots_txt = models.TextField(blank=True)

    root_page = models.ForeignKey(
        Page,
        related_name="+",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # TODO: Language
    # TODO: Parameters. Used for Google Analytics, and others

    def __str__(self) -> str:
        return self.name
