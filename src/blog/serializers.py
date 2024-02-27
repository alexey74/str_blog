"""DRF serializers for the Blog app."""

from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class JPHPostSerializer(PostSerializer):
    id = serializers.IntegerField()
    userId = serializers.IntegerField(source="user_id")

    class Meta(PostSerializer.Meta):
        extra_kwargs = {
            "user_id": {"write_only": True},
        }


class JPHCommentSerializer(CommentSerializer):
    id = serializers.IntegerField()
    postId = serializers.PrimaryKeyRelatedField(
        source="post", queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        
        exclude = ["post"]
        extra_kwargs = {
            "post": {"write_only": True},
        }
