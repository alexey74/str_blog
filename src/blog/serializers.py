"""DRF serializers for the Blog app."""

from typing import Any

from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BulkSavingSerializer(serializers.ListSerializer):
    MAX_BATCH_SIZE = 100

    def create(self, validated_data: dict) -> Any:
        if self.child:
            model_class = getattr(self.child.Meta, "model")
            instances = [model_class(**item) for item in validated_data]
            return model_class.objects.bulk_create(
                instances, batch_size=self.MAX_BATCH_SIZE
            )


class JPHPostSerializer(PostSerializer):
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
