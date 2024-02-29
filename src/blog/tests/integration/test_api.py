from typing import Any, Dict

import pytest
from blog.models import Post
from blog.serializers import PostSerializer
from ddf import G
from django.conf import settings
from django.contrib.auth import get_user_model
from pytest_drf import (
    AsUser,
    Returns200,
    ReturnsLimitOffsetPagination,
    UsesGetMethod,
    UsesListEndpoint,
    ViewSetTest,
)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture

User = get_user_model()


def express_post(post: Post) -> Dict[str, Any]:
    return PostSerializer(post).data


express_posts = pluralized(express_post)


@pytest.fixture
def admuser():
    return G(User)


@pytest.mark.django_db
class TestPostModelViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("post-list"))

    detail_url = lambda_fixture(lambda post: url_for("post-detail", post.pk))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
        ReturnsLimitOffsetPagination,
        AsUser("admuser"),
    ):
        posts = lambda_fixture(
            lambda: G(Post, n=settings.REST_FRAMEWORK["PAGE_SIZE"] - 1),
            autouse=True,
        )

        def test_list_returns_all_posts_sorted(self, posts, results):
            assert results == express_posts(sorted(posts, key=lambda post: post.pk))
