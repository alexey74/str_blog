from celery import shared_task
from celery.utils.log import get_task_logger

from .mixins.jsonplaceholder import JSONPlaceholderPushMixin

log = get_task_logger(__name__)


class Pusher(JSONPlaceholderPushMixin):
    pass


@shared_task
def push_to_jsonplaceholder() -> None:
    log.info("Starting full push...")
    pusher = Pusher()
    result = pusher.push_all()
    log.info("Full push finished, result=%s", result)
