from typing import Any

from blog.mixins.jsonplaceholder import JSONPlaceholderImportMixin, NotEmptyError
from django.core.management.base import BaseCommand, CommandError


class Command(JSONPlaceholderImportMixin, BaseCommand):
    help = """
    Imports data from JSON placeholder API.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            self.import_all()
        except NotEmptyError as err:
            raise CommandError(str(err)) from err
