import pytest
from blog.models import Comment, Post
from django.core.management import CommandError, call_command
from django_dynamic_fixture import G
from jsonplaceholder.client import JSONPlaceholderClient


@pytest.mark.django_db
def test_import_jph_creates_right_records(mocker):
    mock_get_all = mocker.patch.object(
        JSONPlaceholderClient,
        "get_all",
        side_effect=[
            [
                {"id": 42, "userId": 1, "title": "A" * 255, "body": "X" * 2048},
                {"id": 99, "userId": 11, "title": "B" * 25, "body": "Y" * 2048},
            ],
            [
                {
                    "id": 442,
                    "postId": 42,
                    "name": "A" * 255,
                    "email": "u1@example.com",
                    "body": "X" * 2048,
                },
                {
                    "id": 199,
                    "postId": 99,
                    "name": "B" * 25,
                    "email": "u2@example.com",
                    "body": "Y" * 2048,
                },
            ],
        ],
    )

    call_command("import_jph")

    mock_get_all.assert_called()
    assert list(
        Post.objects.all().order_by("id").values("id", "user_id", "title", "body")
    ) == [
        {"id": 42, "user_id": 1, "title": "A" * 255, "body": "X" * 2048},
        {"id": 99, "user_id": 11, "title": "B" * 25, "body": "Y" * 2048},
    ]
    assert list(
        Comment.objects.all()
        .order_by("id")
        .values("id", "post_id", "name", "email", "body")
    ) == [
        {
            "id": 199,
            "post_id": 99,
            "name": "B" * 25,
            "email": "u2@example.com",
            "body": "Y" * 2048,
        },
        {
            "id": 442,
            "post_id": 42,
            "name": "A" * 255,
            "email": "u1@example.com",
            "body": "X" * 2048,
        },
    ]


@pytest.mark.django_db
def test_import_jph_balks_if_fact_tables_not_empty(mocker):
    G(Comment)

    with pytest.raises(CommandError):
        call_command("import_jph")
