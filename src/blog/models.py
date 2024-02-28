"""Module providing core models for the Blog app."""

from django.db import models
from django.conf import settings

from .abstract_models import TimeStampedModel


class Post(TimeStampedModel):
    """Blog post model."""

    # TODO: use a FK here
    user_id = models.PositiveBigIntegerField(
        "User ID",
        default=settings.DEFAULT_USER_ID,
        help_text="Original poster ID",
    )
    title = models.CharField(
        max_length=255, help_text="Short summary of this blog post"
    )
    body = models.TextField(help_text="Full content of this blog post")

    class Meta:
        ordering = ["pk"]

    def __str__(self) -> str:
        return f"{self.title}"


class Comment(TimeStampedModel):
    """Blog post comment model."""

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        help_text="The blog post for which the comment was made.",
    )
    name = models.CharField(max_length=255, help_text="Commenter's name")
    email = models.EmailField(help_text="Commenter's email address")
    body = models.TextField(help_text="Full content of this comment")

    class Meta:
        ordering = ["pk"]

    def __str__(self) -> str:
        return f"{self.name}<{self.email}>: {self.body!s:.80}"


class SyncLog(TimeStampedModel):
    success = models.BooleanField(null=True, blank=True)
    record_count = models.PositiveBigIntegerField(default=0)
    end_date = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["pk"]
