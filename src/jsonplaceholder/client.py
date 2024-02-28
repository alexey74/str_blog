from typing import Any
from apiclient import (
    APIClient,
    endpoint,
    retry_request,
    JsonResponseHandler,
    JsonRequestFormatter,
)


@endpoint(base_url="https://jsonplaceholder.typicode.com")
class Endpoint:
    posts = "posts"
    post = "posts/{id}"
    comments = "comments"
    comment = "comments/{id}"


class JSONPlaceholderClient(APIClient):
    """
    JSON Placeholder fake API client.
    """

    def __init__(self, *args, **kw) -> None:
        super().__init__(
            *args,
            **kw
            | dict(
                response_handler=JsonResponseHandler,
                request_formatter=JsonRequestFormatter,
            )
        )

    @retry_request
    def get_one(self, model: str, oid: int) -> dict:
        url = getattr(Endpoint, model).format(id=oid)
        return self.get(url)

    @retry_request
    def get_all(self, model: str) -> dict:
        return self.get(getattr(Endpoint, model + "s"))

    def put_one(self, model: str, data: dict) -> Any:
        oid = data["id"]
        url = getattr(Endpoint, model).format(id=oid)
        return self.put(url, data)
