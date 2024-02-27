from typing import Dict, Any
import pytest
from pytest_drf import (
    ViewSetTest,
    Returns200,
    Returns201,
    Returns204,
    UsesGetMethod,
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesListEndpoint,
    UsesPatchMethod,
    UsesPostMethod,
    AsUser,
    ReturnsLimitOffsetPagination,
)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture
from ddf import G
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from blog.models import Post


User = get_user_model()


def express_post(post: Post) -> Dict[str, Any]:
    return {
        "id": post.id,
        "user_id": post.user_id,
        "title": post.title,
        "body": post.body,
    }


express_posts = pluralized(express_post)


@pytest.fixture
def admuser():
    user = G(User)
    G(Token, user=user)
    return User


@pytest.mark.django_db
class TestPostModelViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("post-list"))

    detail_url = lambda_fixture(lambda post: url_for("post-detail", post.pk))

    class TestList(UsesGetMethod, UsesListEndpoint, Returns200, ReturnsLimitOffsetPagination, AsUser("admuser")):
        posts = lambda_fixture(
            lambda: G(Post, n=50),
            autouse=True,
        )

        def test_list_returns_all_posts_sorted(self, posts, results):
            assert results == express_posts(sorted(posts, key=lambda post: post.pk))
