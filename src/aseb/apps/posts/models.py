from django.db import models, transaction
from django.utils.timezone import now

from aseb.apps.organization.models import RelatedTopicField
from aseb.core.db.fields import UUIDPrimaryKey
from aseb.core.db.models.base import AuditedModel, User, WebPageModel
from aseb.core.db.utils import UploadToFunction

post_image_upload = UploadToFunction("post/{obj.pk}/{filename}.{ext}")


class Post(AuditedModel, WebPageModel):
    class Type(models.TextChoices):
        text = "text", "Text"
        link = "link", "Link"
        image = "image", "Image"

    id = UUIDPrimaryKey()
    topics = RelatedTopicField()
    type = models.CharField(max_length=10, choices=Type.choices)
    score = models.IntegerField(default=1)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def vote(self, user: User) -> None:
        vote, created = Vote.objects.get_or_create(user=user, post=self)

        if not created:
            return

        with transaction.atomic():
            post = Post.objects.select_for_update().get(id=self.id)

            gravity = 1.8  # HN Default
            item_hour_age = (now() - post.created_at).seconds / 3600
            score = (post.votes - 1) / pow((item_hour_age + 2), gravity)

            post.votes += 1
            post.score = score
            post.save(update_fields=["score", "votes"])


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_votes")
    created_at = models.DateTimeField(auto_now_add=True)
