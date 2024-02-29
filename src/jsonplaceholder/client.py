"""
JSON Placeholder demo API client module.
"""

from typing import Any

from apiclient import (
    APIClient,
    JsonRequestFormatter,
    JsonResponseHandler,
    endpoint,
    retry_request,
)


@endpoint(base_url="https://jsonplaceholder.typicode.com")
class Endpoint:  # pylint: disable=too-few-public-methods
    """
    Endpoint class.

    Collects all known endpoint paths.
    """

    posts = "posts"
    post = "posts/{id}"
    comments = "comments"
    comment = "comments/{id}"


class JSONPlaceholderClient(APIClient):
    """
    JSON Placeholder demo API client.
    """

    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(
            *args,
            **kw
            | {
                "response_handler": JsonResponseHandler,
                "request_formatter": JsonRequestFormatter,
            }
        )

    @retry_request
    def get_one(self, model: str, oid: int) -> Any:
        """
        Fetch one model object by OID

        Args:
            model (str): model name
            oid (int): object ID

        Returns:
            response data with object details
        """
        url = getattr(Endpoint, model).format(id=oid)
        return self.get(url)

    @retry_request
    def get_all(self, model: str) -> Any:
        """
        Get all model objects.

        Args:
            model (str): model name

        Returns:
             response data with objects
        """
        return self.get(getattr(Endpoint, model + "s"))

    def put_one(self, model: str, data: dict) -> Any:
        """
        Update or create one object.

        Args:
            model (str): model name
            data (dict): data to update/create an object with

        Returns:
            response data
        """
        oid = data["id"]
        url = getattr(Endpoint, model).format(id=oid)
        return self.put(url, data)
