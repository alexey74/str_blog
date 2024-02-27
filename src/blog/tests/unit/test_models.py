from ddf import N

from blog.models import Post, Comment


def test_post__str__returns_title():
    post = N(Post)
    assert post.title == str(post)


def test_comment__str__returns_author_and_body_start():
    comment = N(
        Comment,
        name="Foo Bar",
        email="foobar@example.com",
        body="X" * 500,
        post=N(Post),
    )
    assert str(comment) == "Foo Bar<foobar@example.com>: " + "X" * 80
