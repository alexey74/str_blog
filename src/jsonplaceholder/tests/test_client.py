from jsonplaceholder.client import Endpoint, JSONPlaceholderClient


def test_get_one_calls_right_url(mocker):
    client = JSONPlaceholderClient()
    mock_get = mocker.patch.object(client, "get", return_value={"id": 42})

    result = client.get_one("post", 42)

    mock_get.assert_called_once_with(Endpoint.post.format(id=42))
    assert result == {"id": 42}


def test_get_all_calls_right_url(mocker):
    client = JSONPlaceholderClient()
    mock_get = mocker.patch.object(client, "get", return_value=[{"id": 42}, {"id": 7}])

    result = client.get_all("post")

    mock_get.assert_called_once_with(Endpoint.posts)
    assert result == [{"id": 42}, {"id": 7}]
