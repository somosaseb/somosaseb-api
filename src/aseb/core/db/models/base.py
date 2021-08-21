from functools import partial
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.db.models.functions import Now
from django_editorjs_fields import EditorJsJSONField

from aseb.core.db.utils import UploadToFunction

User = get_user_model()


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} {self.pk=}"

    def update(self, refresh_from_db: bool = True, **kwargs):
        """Shortcut to update the instance using an UPDATE query"""
        queryset = self._default_manager.filter(pk=self.pk)
        queryset.update(**kwargs)

        if refresh_from_db:
            self.refresh_from_db()


UserForeignKey = partial(
    models.ForeignKey,
    User,
    related_name="+",
    on_delete=models.CASCADE,
    null=True,
    blank=True,
)


class AuditedModel(BaseModel):
    created_at = models.DateTimeField(default=Now, editable=False)
    created_by = UserForeignKey(editable=False)

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = UserForeignKey(editable=False)

    removed_at = models.DateTimeField(editable=False, null=True, blank=True)
    removed_by = UserForeignKey(editable=False)

    class Meta:
        abstract = True
        default_permissions = "view", "add", "change", "delete", "remove"

    def remove(self, user: Optional[User] = None) -> None:
        self.removed_at = Now()
        self.removed_by = user
        self.save(update_fields=("removed_at", "removed_by"))


class SingletonManager(models.Manager):
    """Singleton Manager that will manage the cache of the only instance of the model."""

    def __init__(self):
        super().__init__()
        self._cache_initialized = False

    def _init_cache(self):
        if not self._cache_initialized and hasattr(cache, "delete_pattern"):
            cache.delete_pattern("current:*")

    @property
    def _cache_key(self) -> str:
        return f"current:{self.model._meta.app_label}.{self.model._meta.model}"

    def get(self, **kwargs):
        return self.current

    @property
    def current(self):
        self._init_cache()

        if not cache.has_key(self._cache_key):  # noqa: W601
            obj, created = self.get_or_create()
            self.current = obj

        return cache.get(self._cache_key)

    @current.deleter
    def current(self):
        cache.delete(self._cache_key)

    @current.setter
    def current(self, obj: models.Model) -> None:
        cache.set(self._cache_key, obj)


class SingletonModel(models.Model):
    objects = SingletonManager()

    class Meta:
        abstract = True

    def save(self, **kwargs) -> None:
        super().save()
        del type(self).objects.current


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published_at__lte=Now())

    def publish(self, published_by=None):
        return self.update(published_at=Now(), published_by=published_by)

    def unpublish(self):
        return self.update(published_at=None, published_by=None)


class PublishableModel(models.Model):
    published_at = models.DateTimeField(blank=True, null=True, editable=False, db_index=True)
    published_by = UserForeignKey(editable=False)

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True

    @property
    def is_published(self) -> bool:
        if self.published_at is None:
            return False
        return self.published_at <= Now()

    def publish(self, published_by=None) -> None:
        self.published_at = Now()
        self.published_by = published_by
        self.save(update_fields=["published_at", "published_by"])

    def unpublish(self) -> None:
        self.published_at = Now()
        self.published_by = None
        self.save(update_fields=["published_at", "published_by"])


main_image_upload = UploadToFunction("{model_name}/{obj.pk}/{filename}.{ext}")


class WebPageModel(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    main_image = models.ImageField(upload_to=main_image_upload, null=True, blank=True)
    content = EditorJsJSONField(blank=True, null=True)

    class Meta:
        abstract = True
