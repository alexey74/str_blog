from celery import shared_task
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)

from .mixins.jsonplaceholder import (
    JSONPlaceholderPushMixin,
)


class Pusher(JSONPlaceholderPushMixin):
    pass


@shared_task
def push_to_jsonplaceholder():
    log.info("Starting full push...")
    pusher = Pusher()
    result = pusher.push_all()
    log.info("Full push finished, result=%s", result)
