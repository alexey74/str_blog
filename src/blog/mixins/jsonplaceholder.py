"""
Module containing mixins for using JSON Placeholder API in a DRF project.
"""

import datetime
import logging
from collections import namedtuple
from typing import Any, Dict

from apiclient.exceptions import APIClientError
from django.db import transaction
from django.utils import timezone
from django_stubs_ext import QuerySetAny

from blog.models import Comment, Post, SyncLog
from blog.serializers import JPHCommentSerializer, JPHPostSerializer
from jsonplaceholder.client import JSONPlaceholderClient

EndPoint = namedtuple("EndPoint", ["model", "serializer_class"])

log = logging.getLogger(__name__)


class NotEmptyError(Exception):
    """
    An Exception raised when DB already contains records
    in tables to be filled during import.
    """

    def __str__(self) -> str:
        return "Database tables not empty, refusing import."


class JSONPlaceholderAdapterMixin:  # pylint: disable=too-few-public-methods
    """
    A base mixin for JSONPlaceholder API support.

    Provides an API client instance.
    """

    # Must be sorted in dependency order.
    ENDPOINTS = {
        "post": EndPoint(Post, JPHPostSerializer),
        "comment": EndPoint(Comment, JPHCommentSerializer),
    }

    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)
        self._client: JSONPlaceholderClient | None = None

    @property
    def client(self) -> JSONPlaceholderClient:
        """
        Return a JSON placeholder API client instance.

        Returns:
            JSONPlaceholderClient: client instance.
        """
        if self._client is None:
            self._client = JSONPlaceholderClient()
        return self._client


class JSONPlaceholderImportMixin(JSONPlaceholderAdapterMixin):
    """
    A mixin class providing functionality to import data
    from JSON Placeholder API.
    """

    MAX_BATCH_SIZE = 100

    def check_import_possible(self) -> None:
        """
        Check if importing data is possible at this point.

        Raises an exception if import is not possible.

        Raises:
            NotEmptyError: relevant DB tables are not empty
        """
        if any(ep.model.objects.count() for ep in self.ENDPOINTS.values()):
            raise NotEmptyError

    def import_resource(self, endpoint: str) -> None:
        """
        Import all records from a single resource endpoint.

        Args:
            endpoint (str): endpoint name
        """
        resource = self.ENDPOINTS[endpoint]
        serializer = resource.serializer_class(
            data=self.client.get_all(endpoint), many=True
        )
        # improve robustness: if validation fails, import valid records only
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def import_all(self) -> None:
        """
        Do a full import.

        Import all records from all known endpoints, if possible.
        Otherwise, raise an exception.
        """
        self.check_import_possible()
        with transaction.atomic():
            for endpoint in self.ENDPOINTS:
                self.import_resource(endpoint)


class JSONPlaceholderPushMixin(JSONPlaceholderAdapterMixin):
    """
    A mixin supporting pushing to JSON Placeholder API.
    """

    @property
    def last_sync_date(self) -> datetime.datetime | None:
        """
        Timestamp if last successful sync (push).

        Returns:
            datetime.datetime | None: last sync timestamp or `None` if none found
        """
        last_sync = (
            SyncLog.objects.filter(success=True, end_date__isnull=False)
            .order_by("created_date")
            .last()
        )
        return last_sync.created_date if last_sync else None

    def push_by_queryset(self, queryset: QuerySetAny) -> Dict[str, Any]:
        """
        Push records from a given queryset.

        Infers API model name from queryset model, then pushes records to the
        matching endpoint.

        Args:
            queryset (QuerySetAny): source queryset with instances to be pushed

        Returns:
            Dict[str, Any]: summary report with pushed record count and error messages
        """
        endpoint = [
            name for name, ep in self.ENDPOINTS.items() if ep.model is queryset.model
        ][0]
        return self.push_resource(endpoint, queryset)

    def push_by_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """
        Push all records from a model to the corresponding remote API endpoint.

        Args:
            endpoint (str): endpoint name to push to

        Returns:
            Dict[str, Any]: summary report with pushed record count and error messages
        """
        resource = self.ENDPOINTS[endpoint]
        queryset = resource.model.objects.all()
        return self.push_resource(endpoint, queryset)

    def push_resource(self, endpoint: str, queryset: QuerySetAny) -> Dict[str, Any]:
        """
        Push records from a given queryset to the specified endpoint.

        Checks if there was a successful sync before,
        abd if yes, selects only records modified after that sync,
        otherwise selects all records.
        After that the method locks selected records, serializes them,
        and pushes one-by-one to the given endpoint, checking for
        errors in the process and collecting operations report.

        Args:
            endpoint (str): endpoint name to push to
            queryset (QuerySetAny): source queryset with records to push

        Returns:
            Dict[str, Any]: summary report with pushed record count and error messages
        """
        resource = self.ENDPOINTS[endpoint]
        count = 0
        errors = []
        with transaction.atomic():
            if self.last_sync_date:
                queryset = queryset.filter(modified_date__gte=self.last_sync_date)
            queryset = queryset.select_for_update()  # lock records
            serializer = resource.serializer_class(queryset, many=True)

            for obj in serializer.data:
                try:
                    log.debug("Pushing to %s: %s", endpoint, obj)
                    self.client.put_one(endpoint, obj)
                except APIClientError as err:
                    errors.append({"obj": obj, "message": str(err)})
                else:
                    count += 1  # type: ignore
        return {"count": count, "errors": errors}

    def push_all(self) -> Dict[str, Any]:
        """
        Push all relevant records from all endpoints.

        Creates a sync log record, iterates over endpoints,
        and pushes records from each of them, collecting
        operations report.

        Returns:
            Dict[str, Any]: summary report with pushed record count and error messages
        """
        log_record = SyncLog.objects.create()
        result = {}
        count = 0
        for endpoint in self.ENDPOINTS:
            result[endpoint] = self.push_by_endpoint(endpoint)
            count += result[endpoint]["count"]
        SyncLog.objects.filter(pk=log_record.pk).update(
            end_date=timezone.now(), record_count=count, result=result, success=True
        )
        result["count"] = count  # type: ignore
        return result
