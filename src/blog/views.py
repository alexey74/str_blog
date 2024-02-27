"""Module providing views for the Blog app."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostModelViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination


class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination
