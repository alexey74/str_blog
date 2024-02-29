"""DRF serializers for the Blog app."""

from typing import Any

from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """
    Post model serializer class.
    """

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment model serializer class.
    """

    class Meta:
        model = Comment
        fields = "__all__"


class BulkSavingSerializer(
    serializers.ListSerializer
):  # pylint: disable=abstract-method
    """
    Serializer class that uses `bulk_create()` to optimize
    saving a batch of instances.

    Use it as a `Meta.list_serializer_class` in other serializers.
    """

    MAX_BATCH_SIZE = 100
    """Size of the batch of instances for bulk creation."""

    def create(self, validated_data: dict) -> Any:
        if self.child:
            model_class = getattr(self.child.Meta, "model")
            instances = [model_class(**item) for item in validated_data]
            return model_class.objects.bulk_create(
                instances, batch_size=self.MAX_BATCH_SIZE
            )
        return None


class JPHPostSerializer(PostSerializer):
    """
    Post model serializer class with JSON Placeholder API format support.
    """

    id = serializers.IntegerField()
    userId = serializers.IntegerField(source="user_id")

    class Meta:
        model = Post
        exclude = ["created_date", "modified_date"]
        extra_kwargs = {
            "user_id": {"write_only": True},
        }
        list_serializer_class = BulkSavingSerializer


class JPHCommentSerializer(CommentSerializer):
    """
    Comment model serializer class with JSON Placeholder API format support.
    """

    id = serializers.IntegerField()
    postId = serializers.PrimaryKeyRelatedField(
        source="post", queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        exclude = ["post", "created_date", "modified_date"]
        extra_kwargs = {
            "post": {"write_only": True},
        }
        list_serializer_class = BulkSavingSerializer
