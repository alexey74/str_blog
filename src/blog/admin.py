"""Module providing admin UI for the Blog app."""

from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.admin import TokenAdmin
from django_object_actions import (
    DjangoObjectActions,
    action,
    takes_instance_or_queryset,
)

from .mixins.jsonplaceholder import (
    JSONPlaceholderImportMixin,
    JSONPlaceholderPushMixin,
    NotEmptyError,
)
from .models import Post, Comment, SyncLog
from .tasks import push_to_jsonplaceholder

TokenAdmin.raw_id_fields = ["user"]


class SyncableAdminMixin(
    JSONPlaceholderImportMixin,
    JSONPlaceholderPushMixin,
    DjangoObjectActions,
    admin.ModelAdmin,
):
    @action(
        label="Import from JPH",
        description="Import all records from JSON Placeholder API",
    )
    def import_from_jsonplaceholder(self, request, obj):
        try:
            self.import_all()
        except NotEmptyError as err:
            self.message_user(request, _("Failed to import: %s" % err), messages.ERROR)
        else:
            self.message_user(
                request,
                _("Import succeeded."),
                messages.SUCCESS,
            )

    @takes_instance_or_queryset
    @action(
        label="Push to JPH",
        description="Push selected records to JSON Placeholder API",
    )
    def push_to_jsonplaceholder(self, request, queryset):
        if queryset:
            result = self.push_by_queryset(queryset)
            msg = _("Pushed %d recs, result: %s" % (queryset.count(), result))

            self.message_user(
                request,
                msg,
                messages.SUCCESS,
            )

    changelist_actions = ("import_from_jsonplaceholder",)
    change_actions = ("import_from_jsonplaceholder", "push_to_jsonplaceholder")
    actions = ("push_to_jsonplaceholder",)


@admin.register(Post)
class PostAdmin(SyncableAdminMixin, admin.ModelAdmin):
    """Blog post model admin configuration."""

    list_display = ("id", "user_id", "title", "created_date")


@admin.register(Comment)
class CommentAdmin(SyncableAdminMixin, admin.ModelAdmin):
    """Blog post comment model admin configuration."""

    list_display = ("id", "post", "name", "email", "created_date", "body")


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    """Sync log model admin configuration."""

    list_display = (
        "id",
        "created_date",
        "end_date",
        "success",
        "record_count",
        "result",
    )

    @action(
        label="Full push to JPH",
        description="Push all records to JSON Placeholder API",
    )
    def push_all_to_jsonplaceholder(self, request, _):
        push_to_jsonplaceholder.delay()
        msg = "Started full push in the background, watch the sync log for results."
        self.message_user(
            request,
            msg,
            messages.SUCCESS,
        )
        
    changelist_actions = ("push_all_to_jsonplaceholder",)
