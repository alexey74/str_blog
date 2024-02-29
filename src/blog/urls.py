"""
URLs module for the Blog app.
"""

from django.urls import include, path
from rest_framework import routers

from .views import CommentModelViewSet, PostModelViewSet

router = routers.DefaultRouter()
router.register(r"post", PostModelViewSet)
router.register(r"comment", CommentModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
