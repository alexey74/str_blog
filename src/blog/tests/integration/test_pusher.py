import pytest
from ddf import G

from blog.models import Comment
from blog.tasks import push_to_jsonplaceholder


@pytest.mark.django_db
def test_full_push_sends_all_records_if_no_sync_found(mocker):
    put_mock = mocker.patch("apiclient.APIClient.put")
    G(Comment, n=10)

    push_to_jsonplaceholder()

    put_mock.assert_called()
    assert put_mock.call_count == 20


@pytest.mark.django_db
def test_full_push_only_sends_records_modified_since_last_push(mocker):
    put_mock = mocker.patch("apiclient.APIClient.put")
    old_comments = G(Comment, n=10)
    push_to_jsonplaceholder()
    G(Comment, n=3)
    old_comments[1].body = "XXXXX"
    old_comments[1].save()
    old_comments[2].post.title = "YYYYYY"
    old_comments[2].post.save()
    put_mock.reset_mock()

    push_to_jsonplaceholder()

    put_mock.assert_called()
    assert put_mock.call_count == 8
