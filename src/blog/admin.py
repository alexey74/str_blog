"""Module providing admin UI for the Blog app."""

from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Post, Comment


TokenAdmin.raw_id_fields = ["user"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Blog post model admin configuration."""


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Blog post comment model admin configuration."""
