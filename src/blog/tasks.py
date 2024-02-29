"""
Celery tasks for the Blog app .
"""

from celery import shared_task
from celery.utils.log import get_task_logger

from .mixins.jsonplaceholder import JSONPlaceholderPushMixin

log = get_task_logger(__name__)


class Pusher(JSONPlaceholderPushMixin):
    """
    JSON Placeholder API pusher class.
    """


@shared_task
def push_to_jsonplaceholder() -> None:
    """
    Perform a full push to JSON Placeholder API.
    """
    log.info("Starting full push...")
    pusher = Pusher()
    result = pusher.push_all()
    log.info("Full push finished, result=%s", result)
