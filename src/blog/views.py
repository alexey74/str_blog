"""Module providing views for the Blog app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostModelViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination


class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.djhtml")
