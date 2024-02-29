import datetime
import logging
from collections import namedtuple
from typing import Any, Dict

from apiclient.exceptions import APIClientError
from blog.models import Comment, Post, SyncLog
from blog.serializers import JPHCommentSerializer, JPHPostSerializer
from django.db import transaction
from django.utils import timezone
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


class JSONPlaceholderAdapterMixin:
    # Must be sorted in dependency order.
    ENDPOINTS = {
        "post": EndPoint(Post, JPHPostSerializer),
        "comment": EndPoint(Comment, JPHCommentSerializer),
    }

    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)
        self._client: JSONPlaceholderClient | None = None

    def check_import_possible(self) -> None:
        if any(ep.model.objects.count() for ep in self.ENDPOINTS.values()):
            raise NotEmptyError

    @property
    def client(self) -> JSONPlaceholderClient:
        if self._client is None:
            self._client = JSONPlaceholderClient()
        return self._client


class JSONPlaceholderImportMixin(JSONPlaceholderAdapterMixin):

    MAX_BATCH_SIZE = 100

    def import_resource(self, endpoint: str) -> None:
        resource = self.ENDPOINTS[endpoint]
        serializer = resource.serializer_class(
            data=self.client.get_all(endpoint), many=True
        )
        # TODO: robustness: if validation fails, import valid records only
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def import_all(self) -> None:
        self.check_import_possible()
        with transaction.atomic():
            for endpoint in self.ENDPOINTS:
                self.import_resource(endpoint)


class JSONPlaceholderPushMixin(JSONPlaceholderAdapterMixin):

    @property
    def last_sync_date(self) -> datetime.datetime | None:
        last_sync = (
            SyncLog.objects.filter(success=True, end_date__isnull=False)
            .order_by("created_date")
            .last()
        )
        return last_sync.created_date if last_sync else None

    def push_by_queryset(self, queryset: Any) -> Dict[str, Any]:
        endpoint = [
            name for name, ep in self.ENDPOINTS.items() if ep.model is queryset.model
        ][0]
        return self.push_resource(endpoint, queryset)

    def push_by_endpoint(self, endpoint: str) -> Dict[str, Any]:
        resource = self.ENDPOINTS[endpoint]
        queryset = resource.model.objects.all()
        return self.push_resource(endpoint, queryset)

    def push_resource(self, endpoint: str, queryset: Any) -> Dict[str, Any]:
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
