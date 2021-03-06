# Generated by Django 3.2.6 on 2021-08-28 03:26

import aseb.core.db.fields
import aseb.core.db.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.datetime
import django_editorjs_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Serie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.db.models.functions.datetime.Now, editable=False
                    ),
                ),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("removed_at", models.DateTimeField(blank=True, editable=False, null=True)),
                ("title", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("seo_title", models.CharField(blank=True, max_length=70)),
                ("seo_description", models.CharField(blank=True, max_length=300)),
                (
                    "main_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=aseb.core.db.utils.UploadToFunction(
                            "{model_name}/{obj.pk}/{filename}.{ext}"
                        ),
                    ),
                ),
                ("content", django_editorjs_fields.fields.EditorJsJSONField(blank=True, null=True)),
                ("headline", models.CharField(blank=True, max_length=140)),
                ("presentation", models.TextField(blank=True)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "removed_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "topics",
                    models.ManyToManyField(
                        blank=True, related_name="_events_serie_topics_+", to="organization.Topic"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "default_permissions": ("view", "add", "change", "delete", "remove"),
            },
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.db.models.functions.datetime.Now, editable=False
                    ),
                ),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("removed_at", models.DateTimeField(blank=True, editable=False, null=True)),
                (
                    "published_at",
                    models.DateTimeField(blank=True, db_index=True, editable=False, null=True),
                ),
                ("title", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("seo_title", models.CharField(blank=True, max_length=70)),
                ("seo_description", models.CharField(blank=True, max_length=300)),
                (
                    "main_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=aseb.core.db.utils.UploadToFunction(
                            "{model_name}/{obj.pk}/{filename}.{ext}"
                        ),
                    ),
                ),
                ("content", django_editorjs_fields.fields.EditorJsJSONField(blank=True, null=True)),
                (
                    "id",
                    aseb.core.db.fields.UUIDField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("headline", models.CharField(blank=True, max_length=140)),
                ("presentation", models.TextField(blank=True)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
                ("duration", models.IntegerField(blank=True, null=True)),
                (
                    "audience",
                    models.CharField(
                        choices=[
                            ("public", "Public"),
                            ("members", "Member"),
                            ("partners", "Partners"),
                        ],
                        max_length=10,
                    ),
                ),
                ("capacity", models.IntegerField(blank=True, null=True)),
                (
                    "location_type",
                    models.CharField(
                        choices=[("place", "Place"), ("virtual", "Virtual")], max_length=10
                    ),
                ),
                ("location_address", models.CharField(blank=True, max_length=300)),
                ("location_url", models.URLField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "published_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "removed_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "serie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="events.serie",
                    ),
                ),
                (
                    "topics",
                    models.ManyToManyField(
                        blank=True, related_name="_events_event_topics_+", to="organization.Topic"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EventPerformer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_performers",
                        to="events.event",
                    ),
                ),
                (
                    "performer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="performed_events",
                        to="organization.member",
                    ),
                ),
            ],
            options={
                "unique_together": {("performer", "event")},
            },
        ),
        migrations.CreateModel(
            name="EventOrganizer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events_organizers",
                        to="events.event",
                    ),
                ),
                (
                    "organizer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="organized_events",
                        to="organization.member",
                    ),
                ),
            ],
            options={
                "unique_together": {("organizer", "event")},
            },
        ),
    ]
