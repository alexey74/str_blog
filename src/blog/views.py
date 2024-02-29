"""Module providing views for the Blog app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from .base_views import BaseViewSet
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostModelViewSet(BaseViewSet):
    """
    Blog post.

    Represents posts to the blog by users.
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination


class CommentModelViewSet(BaseViewSet):
    """
    Comment to a blog post.

    Represents comments made by users to blog posts.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination


def index(request: HttpRequest) -> HttpResponse:
    """
    The home page view.

    Args:
        request (HttpRequest): HTTP request causing this call

    Returns:
        HttpResponse: response data with home page rendered.
    """
    return render(request, "index.djhtml")
