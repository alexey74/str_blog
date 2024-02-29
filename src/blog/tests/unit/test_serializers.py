import pytest
from blog.models import Post
from blog.serializers import JPHCommentSerializer, JPHPostSerializer
from django_dynamic_fixture import G


def test_jph_post_serializer_maps_correct_field_values_for_bulk_data():
    serializer = JPHPostSerializer(
        data=[
            {"id": 42, "userId": 1, "title": "A" * 255, "body": "X" * 2048},
            {"id": 99, "userId": 11, "title": "B" * 25, "body": "Y" * 2048},
        ],
        many=True,
    )

    assert serializer.is_valid()

    assert [dict(item) for item in serializer.validated_data] == [
        {"id": 42, "user_id": 1, "title": "A" * 255, "body": "X" * 2048},
        {"id": 99, "user_id": 11, "title": "B" * 25, "body": "Y" * 2048},
    ]


@pytest.mark.django_db
def test_jph_comment_serializer_maps_correct_field_values_for_bulk_data():
    serializer = JPHCommentSerializer(
        data=[
            {
                "id": 42,
                "postId": 1,
                "name": "A" * 255,
                "email": "u1@example.com",
                "body": "X" * 2048,
            },
            {
                "id": 99,
                "postId": 11,
                "name": "B" * 25,
                "email": "u2@example.com",
                "body": "Y" * 2048,
            },
        ],
        many=True,
    )
    post1 = G(Post, id=1)
    post11 = G(Post, id=11)

    serializer.is_valid(raise_exception=True)

    assert [dict(item) for item in serializer.validated_data] == [
        {
            "id": 42,
            "post": post1,
            "name": "A" * 255,
            "email": "u1@example.com",
            "body": "X" * 2048,
        },
        {
            "id": 99,
            "post": post11,
            "name": "B" * 25,
            "email": "u2@example.com",
            "body": "Y" * 2048,
        },
    ]
