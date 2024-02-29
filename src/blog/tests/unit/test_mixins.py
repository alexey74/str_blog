from apiclient.exceptions import APIClientError
from blog.mixins.jsonplaceholder import JSONPlaceholderPushMixin
from blog.models import Post
from ddf import G


class JSONPlaceholderPusher(JSONPlaceholderPushMixin):
    pass


def test_push_resource_reports_api_errors(mocker, db):
    pusher = JSONPlaceholderPusher()
    put_mock = mocker.patch.object(
        pusher.client, "put_one", side_effect=APIClientError("foo")
    )
    G(Post)

    result = pusher.push_resource("post", Post.objects.all())

    put_mock.assert_called()
    assert result["count"] == 0
    assert result["errors"][0]["message"] == "foo"


def test_push_by_queryset_selects_correct_endpoint(mocker, db):
    pusher = JSONPlaceholderPusher()
    push_mock = mocker.patch.object(
        pusher,
        "push_resource",
    )
    G(Post)

    pusher.push_by_queryset(Post.objects.all())

    push_mock.assert_called()
    assert push_mock.call_args[0][0] == "post"
