import pytest
from ddf import G
from django.contrib import messages
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import reverse
from django.test import RequestFactory

from blog.admin import PostAdmin, SyncLogAdmin
from blog.mixins.jsonplaceholder import NotEmptyError
from blog.models import Post, SyncLog

User = get_user_model()


@pytest.fixture
def site():
    return AdminSite()


@pytest.fixture(scope="function", params=["post", "comment"])
def admin_request(request, db) -> HttpRequest:
    factory = RequestFactory()
    superuser = User.objects.create_superuser(username="superuser", is_staff=True)
    url = reverse(f"admin:blog_{request.param}_changelist")
    superuser_request = factory.get(url)
    superuser_request.user = superuser

    return superuser_request


@pytest.mark.django_db
def test_import_from_jsonplaceholder_informs_user_on_success(
    mocker, site, admin_request
):
    post_admin = PostAdmin(Post, site)
    import_all_mock = mocker.patch.object(post_admin, "import_all")
    message_mock = mocker.patch.object(post_admin, "message_user")

    post_admin.import_from_jsonplaceholder(admin_request)

    import_all_mock.assert_called_once()
    message_mock.assert_called_once()
    assert message_mock.call_args[0][2] == messages.SUCCESS


@pytest.mark.django_db
def test_import_from_jsonplaceholder_reports_error(mocker, site, admin_request):
    post_admin = PostAdmin(Post, site)
    import_all_mock = mocker.patch.object(
        post_admin, "import_all", side_effect=NotEmptyError
    )
    message_mock = mocker.patch.object(post_admin, "message_user")

    post_admin.import_from_jsonplaceholder(admin_request)

    import_all_mock.assert_called_once()
    message_mock.assert_called_once()
    assert message_mock.call_args[0][2] == messages.ERROR


@pytest.mark.django_db
def test_push_to_jsonplaceholder_informs_user_on_success(mocker, site, admin_request):
    post_admin = PostAdmin(Post, site)
    call_mock = mocker.patch.object(post_admin, "push_by_queryset")
    message_mock = mocker.patch.object(post_admin, "message_user")
    G(Post)

    post_admin.push_to_jsonplaceholder(admin_request, Post.objects.all())

    call_mock.assert_called_once()
    message_mock.assert_called_once()
    assert message_mock.call_args[0][2] == messages.SUCCESS


@pytest.mark.django_db
def test_push_all_to_jsonplaceholder_informs_user_on_success(
    mocker, site, admin_request
):
    admin = SyncLogAdmin(SyncLog, site)
    call_mock = mocker.patch("blog.tasks.push_to_jsonplaceholder.delay")
    message_mock = mocker.patch.object(admin, "message_user")

    admin.push_all_to_jsonplaceholder(admin_request, Post.objects.all())

    call_mock.assert_called_once()
    message_mock.assert_called_once()
    assert message_mock.call_args[0][2] == messages.SUCCESS
