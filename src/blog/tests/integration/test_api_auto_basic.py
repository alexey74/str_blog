import pytest
from ddf import G
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Comment, Post

User = settings.AUTH_USER_MODEL


# PostModelViewSet Tests


@pytest.fixture
def user():
    return G(User)


@pytest.fixture
def client(user):
    access_token = G(Token, user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token.key)
    return client


@pytest.fixture
def post():
    return G(Post)


@pytest.fixture
def comment():
    return G(Comment)


@pytest.mark.django_db
def test_post_list_get(client):
    url = reverse("post-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_create_post(client, user):
    url = reverse("post-list")
    response = client.post(
        url,
        data={"title": "foo", "user_id": user.pk, "body": "X" * 2048},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_post_retrieve_get(client, post):
    url = reverse("post-detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_update_put(client, post, user):
    url = reverse("post-detail", kwargs={"pk": post.pk})
    response = client.put(
        url, data={"title": "bar", "user_id": user.pk, "body": "AAAAA"}
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_partial_update_patch(client, post):
    url = reverse("post-detail", kwargs={"pk": post.pk})
    response = client.patch(url, data={"body": "B"})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_destroy_delete(client, post):
    url = reverse("post-detail", kwargs={"pk": post.pk})
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# CommentModelViewSet Tests


@pytest.mark.django_db
def test_comment_list_get(client):
    url = reverse("comment-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_comment_create_post(client, post):
    url = reverse("comment-list")
    response = client.post(
        url,
        data={
            "name": "foo",
            "email": "u123@example.com",
            "post": post.pk,
            "body": "A" * 2048,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_comment_retrieve_get(client, comment):
    url = reverse("comment-detail", kwargs={"pk": comment.pk})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_comment_update_put(client, comment, post):
    url = reverse("comment-detail", kwargs={"pk": comment.pk})
    response = client.put(
        url,
        data={
            "name": "bar",
            "email": "u456@example.com",
            "post": post.pk,
            "body": "B" * 2048,
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_comment_partial_update_patch(client, comment):
    url = reverse("comment-detail", kwargs={"pk": comment.pk})
    response = client.patch(
        url,
        data={
            "email": "u456@example.com",
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_comment_destroy_delete(client, comment):
    url = reverse("comment-detail", kwargs={"pk": comment.pk})
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
