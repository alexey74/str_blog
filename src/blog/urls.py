from django.urls import path, include
from rest_framework import routers

from .views import PostModelViewSet, CommentModelViewSet, index

router = routers.DefaultRouter()
router.register(r"post", PostModelViewSet)
router.register(r"comment", CommentModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
